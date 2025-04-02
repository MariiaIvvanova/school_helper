from datetime import datetime

from sqlalchemy import func

from src.db.model.RatingLiteraryWorks import RatingLiteraryWorks
from src.db.model.Users import Users


class RatingLiteraryWorksRepository:
    def __init__(self, session):
        self.session = session

    def create(self, id_literary_works, id_user, rating):
        now = datetime.now()
        now_date = now.isoformat(timespec='milliseconds')
        new_user = Users(
            id_literary_works=id_literary_works,
            id_user=id_user,
            rating=rating,
            create_date=now_date,
            updata_date=now_date
        )
        self.session.add(new_user)
        self.session.commit()

    def calculate_average_rating(self, work_id):
        # Используем агрегатную функцию AVG для вычисления средней оценки
        average_rating = (self.session.query(func.avg(RatingLiteraryWorks.rating))
                          .filter(RatingLiteraryWorks.work_id == work_id).scalar())
        return average_rating
