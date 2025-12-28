from typing import Optional

try:
    from pydantic_settings import BaseSettings
except Exception:  # pragma: no cover - fallback for test env without pydantic_settings
    try:
        from pydantic import BaseSettings
    except Exception:  # pragma: no cover - if pydantic's BaseSettings is unavailable, provide a minimal shim
        class BaseSettings:  # simple fallback so tests can import the module
            pass

from pydantic import SecretStr, EmailStr, field_validator
from pydantic_core.core_schema import ValidationInfo


class Settings(BaseSettings):
    PROJECT_NAME: str = "TestProject"

    POSTGRES_DB: str = "test_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: SecretStr = SecretStr("test_pass")
    POSTGRES_URI: Optional[str] = None

    FIRST_USER_EMAIL: EmailStr = "test@example.com"
    FIRST_USER_PASSWORD: SecretStr = SecretStr("test_pass")

    SECRET_KEY: SecretStr = SecretStr("supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @field_validator("POSTGRES_URI", mode="before")
    @classmethod
    def build_postgres_uri(
        cls, v: Optional[str], info: ValidationInfo
    ) -> str:
        if isinstance(v, str) and v:
            return v

        data = info.data
        password: SecretStr = data.get("POSTGRES_PASSWORD", SecretStr(""))
        return (
            f"postgresql+asyncpg://"
            f"{data.get('POSTGRES_USER')}:"
            f"{password.get_secret_value()}@"
            f"{data.get('POSTGRES_HOST')}/"
            f"{data.get('POSTGRES_DB')}"
        )


settings = Settings()
