from sqlalchemy import Column, Integer, DateTime, ForeignKey

from src.db.connect import Base


class RatingLiteraryWorks(Base):
    __tablename__  = 'rating_literary_works'

    id = Column(Integer, primary_key=True)
    id_literary_works = Column(Integer, ForeignKey("literary_works.id"))
    id_user = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=True)
    create_date = Column(DateTime)
    updata_date = Column(DateTime)
