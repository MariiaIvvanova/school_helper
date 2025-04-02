from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.db.connect import Base


class Users(Base):
    __tablename__  = 'users'

    id = Column(String, primary_key=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    is_block = Column(Boolean, default=False)
    create_date = Column(DateTime)
    updata_date = Column(DateTime)
