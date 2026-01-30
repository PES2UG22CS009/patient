import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str


def get_settings() -> Settings:
    # 1) Prefer environment variable if user sets it
    url = os.getenv("DATABASE_URL")

    # 2) If not set, try config.local.py (ignored by git)
    if not url:
        try:
            from src.config_local import DATABASE_URL as local_url  # type: ignore

            url = local_url
        except Exception:
            url = None

    if not url:
        raise RuntimeError(
            "DATABASE_URL not found. Set it as an env var or create src/config_local.py "
            "with DATABASE_URL = 'mysql+pymysql://...'"
        )

    return Settings(database_url=url)
