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

    json_logs: bool = True
    db_pool_size: int = 3
    db_max_overflow: int = 2
    db_pool_timeout: int = 10


settings = Settings()