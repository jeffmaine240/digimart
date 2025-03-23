from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Generator

from core.config import config
from models.base_model import Base


# ====== Config & Paths ====== #
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_NAME = config.DB_NAME
DB_TYPE = config.DB_TYPE

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Root directory


# ====== Engine Factory ====== #
def get_db_engine(test_mode: bool = False):
    """
    Create a database engine based on the configuration.
    Args:
        test_mode (bool): Whether to use test database or main database.
    Returns:
        Engine: SQLAlchemy engine instance.
    """
    if DB_TYPE == "sqlite" or test_mode:
        db_path = BASE_DIR / "test.db" if test_mode else BASE_DIR / "main.db"
        DATABASE_URL = f"sqlite:///{db_path}"
        return create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )

    elif DB_TYPE == "postgresql":
        DATABASE_URL = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        return create_engine(DATABASE_URL)

    else:
        raise ValueError("Unsupported DB_TYPE specified in environment")


# ====== Engine and Session ====== #
engine = get_db_engine()
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
db_session = scoped_session(SessionLocal)


# ====== Database Management ====== #
def create_database():
    """
    Creates all tables in the database.
    """
    Base.metadata.create_all(bind=engine)


def drop_database():
    """
    Drops all tables in the database (Dangerous in production!).
    """
    Base.metadata.drop_all(bind=engine)


# ====== Dependency for FastAPI Routes ====== #
def get_db() -> Generator:
    """
    Yields a database session for use in API routes.
    Ensures the session is closed after request.
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()
