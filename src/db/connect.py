from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import Config

config = Config()

Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
