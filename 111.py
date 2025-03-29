from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:yourpassword@localhost:5432"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
class LiteraryWorks(Base):
    __tablename__  = 'literary_works'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    response = Column(String)
    llm = Column(String, default="giga")
    create_date = Column(Date)
    updata_date = Column(Date)


Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

new_user = LiteraryWorks(name="Преступление и наказание",
                         response="Преступление и наказание» — это роман Фёдора Михайловича Достоевского, впервые опубликованный в 1866 году",
                         create_date=datetime.now(),
                         updata_date=datetime.now())
session.add(new_user)
session.commit()