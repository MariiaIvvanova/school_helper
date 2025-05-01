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
        new_rating = RatingLiteraryWorks(
            id_literary_works=id_literary_works,
            id_user=id_user,
            rating=rating,
            create_date=now_date,
            updata_date=now_date
        )
        self.session.add(new_rating)
        self.session.commit()

    def delete_ratings_by_work_id(self, work_id):
        self.session.query(RatingLiteraryWorks).filter(
            RatingLiteraryWorks.id_literary_works == work_id
        ).delete()
        self.session.commit()

    def calculate_average_rating(self, work_id) -> int:
        # Используем агрегатную функцию AVG для вычисления средней оценки
        average_rating = (self.session.query(func.avg(RatingLiteraryWorks.rating))
                          .filter(RatingLiteraryWorks.id_literary_works == work_id).scalar())
        return average_rating

    def count_ratings(self, work_id) -> int:
        # Используем агрегатную функцию COUNT для подсчета количества оценок
        rating_count = (self.session.query(func.count(RatingLiteraryWorks.rating))
                        .filter(RatingLiteraryWorks.id_literary_works == work_id)
                        .scalar())
        return rating_count
