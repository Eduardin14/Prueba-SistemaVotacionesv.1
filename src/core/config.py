"""
Configuracion centralizada (CORS, paginacion) desde variables de entorno.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Ajustes cargados desde el entorno y opcionalmente desde un archivo `.env`."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_ignore_empty=True,
    )

    # Orígenes permitidos separados por coma.
    cors_origins: str = Field(
        default=(
            "http://localhost:3000,"
            "http://localhost:4200,"
            "http://localhost:5173,"
            "http://127.0.0.1:3000,"
            "http://127.0.0.1:4200,"
            "http://127.0.0.1:5173"
        ),
        validation_alias="CORS_ORIGINS",
    )

    default_page_size: int = Field(default=10, ge=1, le=100, validation_alias="DEFAULT_PAGE_SIZE")

    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
