from typing import Optional

try:
    from pydantic_settings import BaseSettings
except Exception:  # pragma: no cover - fallback for test env without pydantic_settings
    try:
        from pydantic import BaseSettings
    except Exception:  # pragma: no cover - if pydantic's BaseSettings is unavailable, provide a minimal shim
        class BaseSettings:  # simple fallback so tests can import the module
            pass

from pydantic import SecretStr, field_validator
from pydantic_core.core_schema import ValidationInfo


class Settings(BaseSettings):
    PROJECT_NAME: str = "OrdersProject"

    POSTGRES_DB: str = "orders_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_USER: str = "orders_user"
    POSTGRES_PASSWORD: SecretStr = SecretStr("orders_pass")
    POSTGRES_URI: Optional[str] = None

    USER_SERVICE_URL: str = "http://localhost:8000/api/v1/internal"

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
