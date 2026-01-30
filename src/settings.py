import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    database_url: str


def get_settings() -> Settings:
    """
    Load configuration in a secure way.

    Production rule:
      - DATABASE_URL must be provided via env var or src/config_local.py

    Test/CI rule:
      - if MEMS_TESTING=1 (or CI=true), allow a safe SQLite fallback so
        tests can run without real secrets.
    """
    # 1) Prefer environment variable
    url = os.getenv("DATABASE_URL")

    # 2) If not set, try local config file (ignored by git)
    if not url:
        try:
            from src.config_local import DATABASE_URL as local_url  # type: ignore

            url = local_url
        except Exception:
            url = None

    # 3) Test/CI fallback (NO secrets required)
    # GitHub Actions typically sets CI=true
    if not url and (os.getenv("MEMS_TESTING") == "1" or os.getenv("CI") == "true"):
        url = "sqlite+pysqlite:///:memory:"

    if not url:
        raise RuntimeError(
            "DATABASE_URL not found. Set it as an env var or create src/config_local.py "
            "with DATABASE_URL = 'mysql+pymysql://...'"
        )

    return Settings(database_url=url)
