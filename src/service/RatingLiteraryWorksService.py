from src.db.connect import get_session
from src.db.repository import RatingLiteraryWorksRepository
from src.db.repository import LiteraryWorksRepository


class RatingLiteraryWorksService:
    def __init__(self, rating_literary_works: RatingLiteraryWorksRepository, literary_repo: LiteraryWorksRepository):
        self.literary_repo = literary_repo(get_session())
        self.rating_literary_works = rating_literary_works(get_session())

    def add_rating(self, telegram_id: str, literary_name: str, rating):
        try:
            liter = self.literary_repo.get_by_name(literary_name)
            return self.rating_literary_works.create(liter.id, telegram_id, rating)
        except Exception as e:
            print(f"Ошибка при добавлении оценки: {str(e)}")
            return None

    def check_udata(self, literary_name: str):
        try:
            liter = self.literary_repo.get_by_name(literary_name)
            if not liter:
                print(f"Произведение '{literary_name}' не найдено.")
                return False

            avg = self.rating_literary_works.calculate_average_rating(liter.id)
            count = self.rating_literary_works.count_ratings(liter.id)

            if avg is None or count == 0:
                # Нет оценок вообще
                return False

            if avg < 0.5 and count >= 3:
                return True
            else:
                return False
        except Exception as e:
            print(f"Ошибка при проверке оценки: {str(e)}")
            return False

