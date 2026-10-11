from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from KNOWITALL_* environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="KNOWITALL_",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = "development"
    log_level: str = "INFO"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    postgres_dsn: str = "postgresql://knowitall:knowitall@127.0.0.1:5432/knowitall"
    redis_url: str = "redis://127.0.0.1:6379/0"
    object_store_backend: str = "local"
    local_object_store_path: str = ".data/objects"
    s3_endpoint: str = "http://127.0.0.1:9000"
    s3_access_key: str = "knowitall"
    s3_secret_key: str = Field(default="change-me", repr=False)
    s3_bucket: str = "knowitall"


@lru_cache
def get_settings() -> Settings:
    return Settings()
