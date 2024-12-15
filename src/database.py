from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///test.db")

def init_db():
    SQLModel.metadata.create_all(engine)
        
def get_session():
    session = sessionmaker(
        bind=engine, class_=Session, expire_on_commit=False
    )

    with session() as session:
        yield session
