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
        # агрегатная функция AVG для вычисления средней оценки
        average_rating = (self.session.query(func.avg(RatingLiteraryWorks.rating))
                          .filter(RatingLiteraryWorks.id_literary_works == work_id).scalar())
        return average_rating

    def count_ratings(self, work_id) -> int:
        # агрегатная функция COUNT для подсчета количества оценок
        rating_count = (self.session.query(func.count(RatingLiteraryWorks.rating))
                        .filter(RatingLiteraryWorks.id_literary_works == work_id)
                        .scalar())
        return rating_count

    def get_user_by_telegram_id(self, telegram_id: str):
        return self.session.query(Users).filter_by(telegram_id=telegram_id).first()

    def get_by_user_and_work(self, user_id: int, work_id: int):
        return self.session.query(RatingLiteraryWorks).filter_by(id_user=user_id, id_literary_works=work_id).first()
