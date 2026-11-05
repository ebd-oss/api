import logging
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlmodel import Session, SQLModel

from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    # SQLCipher: PRAGMA key must be first statement on every new connection
    if settings.DATABASE_ENCRYPTION_KEY and settings.ENVIRONMENT != "test":
        try:
            cursor.execute(f"PRAGMA key = '{settings.DATABASE_ENCRYPTION_KEY}'")
        except Exception as e:
            logger.warning(f"Failed to set SQLCipher key: {e}")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


def get_engine():
    database_url = settings.DATABASE_URL
    connect_args = {"check_same_thread": False}
    
    # Try SQLCipher if key is provided
    if settings.DATABASE_ENCRYPTION_KEY and settings.ENVIRONMENT not in ("test", "development"):
        try:
            # Try sqlcipher3
            engine = create_engine(
                database_url.replace("sqlite:///", "sqlite+pysqlcipher:///?cipher=aes-256-cbc&kdf_iter=64000&cipher_page_size=1024"),
                connect_args=connect_args,
                echo=False,
            )
            event.listen(engine, "connect", _set_sqlite_pragma)
            return engine
        except Exception as e:
            logger.warning(f"SQLCipher driver not available: {e}. Falling back to plain SQLite.")
    
    if settings.DATABASE_ENCRYPTION_KEY and settings.ENVIRONMENT in ("test", "development"):
        logger.warning("DATABASE_ENCRYPTION_KEY set but using plain SQLite in test/development mode")
    
    engine = create_engine(database_url, connect_args=connect_args, echo=False)
    event.listen(engine, "connect", _set_sqlite_pragma)
    return engine


engine = get_engine()


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
