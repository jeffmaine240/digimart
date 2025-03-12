from pathlib import Path
from src.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session



DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_NAME = config.DB_NAME
DB_TYPE = config.DB_TYPE

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_db_engine(test_mode: bool=False):

    if DB_TYPE=="sqlite" or test_mode:
        BASE_PATH = f"sqlite:///{BASE_DIR}"
        DATABASE_URL = BASE_PATH + "/"

        if test_mode:
            DATABASE_URL = BASE_PATH + "test.db"
            return create_engine(
                DATABASE_URL, connect_args={"check_same_thread": False}
            )
        
    elif DB_TYPE=="postgresql":
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 

    return create_engine(
        url=DATABASE_URL,
        echo=True
    )


engine = get_db_engine()

SessionLocal = sessionmaker(
                    autocommit=False, 
                    autoflush=False, 
                    bind=engine
                )

db_session = scoped_session(SessionLocal)

Base = declarative_base()


def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
