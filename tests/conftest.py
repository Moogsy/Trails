import os

# Seed required env vars before any app module is imported.
# pydantic-settings reads these at Settings() instantiation time.
for _key, _val in {
    "DATABASE_URL": "postgresql+asyncpg://localhost/trails_test",
    "REDIS_URL": "redis://localhost:6379",
    "SECRET_KEY": "test-secret-key",
    "PHONE_HASH_SECRET": "test-phone-hash",
    "DEVICE_HASH_SECRET": "test-device-hash",
}.items():
    os.environ.setdefault(_key, _val)
