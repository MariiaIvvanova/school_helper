from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.db.connect import Base
from src.db.model.constants import UserRole


class Users(Base):
    __tablename__  = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(String, default=UserRole.BASIC)
    is_block = Column(Boolean, default=False)
    create_date = Column(DateTime)
    updata_date = Column(DateTime)
