from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    JWT_SECRET_KEY: str = secrets.token_urlsafe(64)
    JWT_ALGORITHM: str = "HS256"
    model_config = SettingsConfigDict(env_file=".env")
    REDIS_URL: str
    SENTRY_DSN: str

settings = Settings()
