from functools import lru_cache
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from src.config import get_db_url


@lru_cache
def get_engine():
    return create_engine(get_db_url())


def init_db():
    SQLModel.metadata.create_all(get_engine())


def get_session():
    session = sessionmaker(bind=get_engine(), class_=Session, expire_on_commit=False)

    with session() as session:
        yield session
