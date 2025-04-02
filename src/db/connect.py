from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from src.config import config


Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
