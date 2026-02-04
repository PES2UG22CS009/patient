from __future__ import annotations

from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.settings import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """
    Lazily create the SQLAlchemy engine.

    IMPORTANT:
    - Do NOT read settings / DATABASE_URL at import time.
    - This keeps Swagger reachable even if DATABASE_URL isn't set,
      because /docs doesn't need a DB connection to render.
    """
    settings = get_settings()
    return create_engine(
        settings.database_url,
        pool_pre_ping=True,
        pool_recycle=1800,
        echo=False,
        future=True,
    )


def get_sessionmaker():
    return sessionmaker(
        bind=get_engine(),
        autoflush=False,
        autocommit=False,
        future=True,
    )


def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
