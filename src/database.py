from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session
from src.config import DB_URL

engine = create_engine(DB_URL)

def init_db():
    SQLModel.metadata.create_all(engine)
        
def get_session():
    session = sessionmaker(
        bind=engine, class_=Session, expire_on_commit=False
    )

    with session() as session:
        yield session
