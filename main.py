from fastapi import FastAPI
from api.routes import auth, sessions, answers, matches, payments, notifications, health


def create_app() -> FastAPI:
    app = FastAPI(title="Trails API")

    app.include_router(health.router, tags=["health"])
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
    app.include_router(answers.router, prefix="/answers", tags=["answers"])
    app.include_router(matches.router, prefix="/matches", tags=["matches"])
    app.include_router(payments.router, prefix="/payments", tags=["payments"])
    app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

    return app


app = create_app()