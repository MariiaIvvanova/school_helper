from sqlalchemy import Column, Integer, String, Date, DateTime

from src.db.connect import Base


class LiteraryWorks(Base):
    __tablename__  = 'literary_works'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    response = Column(String)
    llm = Column(String, default="giga")
    create_date = Column(DateTime)
    updata_date = Column(DateTime)
