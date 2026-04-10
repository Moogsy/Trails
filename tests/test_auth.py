import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from jose import jwt

from api.deps import get_db
from config import settings
from db import User
from main import app


@pytest.fixture
def mock_db():
    db = AsyncMock()
    db.add = MagicMock()  # sync in SQLAlchemy async session
    return db


@pytest.fixture
def client(mock_db):
    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def _execute_returning(user):
    """Return a mock db.execute result whose scalar_one_or_none gives user."""
    result = MagicMock()
    result.scalar_one_or_none.return_value = user
    return result


def test_verify_creates_new_user(client, mock_db):
    """First login: user doesn't exist yet — should be created and a token returned."""
    user_id = uuid.uuid4()
    mock_db.execute.return_value = _execute_returning(None)

    async def fake_refresh(user):
        user.id = user_id

    mock_db.refresh.side_effect = fake_refresh

    with patch("api.routes.auth._verify_identity_token", return_value="apple|123"):
        resp = client.post("/auth/verify", json={"provider": "apple", "identity_token": "tok"})

    assert resp.status_code == 200
    assert resp.json()["token_type"] == "bearer"
    assert resp.json()["access_token"]
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_verify_returns_existing_user(client, mock_db):
    """Returning user: should be looked up, not re-created."""
    user_id = uuid.uuid4()
    existing = User(id=user_id, oauth_provider="google", oauth_provider_uid="google|456")
    mock_db.execute.return_value = _execute_returning(existing)

    with patch("api.routes.auth._verify_identity_token", return_value="google|456"):
        resp = client.post("/auth/verify", json={"provider": "google", "identity_token": "tok"})

    assert resp.status_code == 200
    mock_db.add.assert_not_called()
    mock_db.commit.assert_not_called()


def test_verify_token_encodes_user_id(client, mock_db):
    """The returned JWT sub claim must match the user's id."""
    user_id = uuid.uuid4()
    existing = User(id=user_id, oauth_provider="apple", oauth_provider_uid="apple|789")
    mock_db.execute.return_value = _execute_returning(existing)

    with patch("api.routes.auth._verify_identity_token", return_value="apple|789"):
        resp = client.post("/auth/verify", json={"provider": "apple", "identity_token": "tok"})

    token = resp.json()["access_token"]
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    assert payload["sub"] == str(user_id)


def test_verify_missing_fields_returns_422(client, mock_db):
    resp = client.post("/auth/verify", json={"provider": "apple"})
    assert resp.status_code == 422
