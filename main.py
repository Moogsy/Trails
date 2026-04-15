import uuid
import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import TimeoutError as SATimeoutError
from config import settings
from logging_setup import configure_logging
from api.routes import auth, sessions, answers, matches, payments, notifications, health


def create_app() -> FastAPI:
    configure_logging(json_logs=settings.json_logs)

    app = FastAPI(title="Trails API")

    @app.middleware("http")
    async def request_id_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

    @app.exception_handler(SATimeoutError)
    async def db_timeout_handler(request: Request, exc: SATimeoutError):
        return JSONResponse(status_code=503, content={"detail": "database unavailable"})

    app.include_router(health.router, tags=["health"])
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
    app.include_router(answers.router, prefix="/answers", tags=["answers"])
    app.include_router(matches.router, prefix="/matches", tags=["matches"])
    app.include_router(payments.router, prefix="/payments", tags=["payments"])
    app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

    return app


app = create_app()