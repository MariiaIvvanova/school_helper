from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

from src.config import config

Base = declarative_base()

def init_db():
    """
    Инициализирует базу данных и создает все таблицы
    """
    engine = create_engine(
        config.DATABASE_URL,
        pool_size=20,
        max_overflow=50,
        pool_timeout=60,
    )
    Base.metadata.create_all(engine)
    return engine

# Создаем движок базы данных
engine = init_db()

Session = sessionmaker(bind=engine)

def get_session():
    return Session()
