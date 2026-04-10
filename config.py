from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    redis_url: str
    secret_key: str

    phone_hash_secret: str
    device_hash_secret: str

    apple_client_id: str = ""
    google_client_id: str = ""

    expo_access_token: str = ""

    sentry_dsn: str = ""

    env: str = "prod"  # "prod" | "test"


settings = Settings()