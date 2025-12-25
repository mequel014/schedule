# ./app/core/db.py

from sqlmodel import create_engine, SQLModel, Session
from .config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def seed_db():
    """Seed database with initial data"""
    from .seed import seed_initial_data
    
    with Session(engine) as session:
        seed_initial_data(session)