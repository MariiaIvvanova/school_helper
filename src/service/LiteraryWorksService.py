from src.db.connect import get_session
from src.db.repository import LiteraryWorksRepository
from src.db.repository.RatingLiteraryWorksRepository import RatingLiteraryWorksRepository
from src.service import RatingLiteraryWorksService
from src.llm.constant import defoult_llm
from src.llm.factory import llm_client


class LiteraryWorksService:
    def __init__(self, literary_repo: LiteraryWorksRepository, rating_literary_works: RatingLiteraryWorksService, rating_literary_works_repo: RatingLiteraryWorksRepository):
        self.literary_repo = literary_repo(get_session())
        self.rating_literary_works = rating_literary_works(rating_literary_works_repo, literary_repo)

    def upsert_literary(self, name: str) -> str:
        try:
            liter = self.literary_repo.get_by_name(name)
            if liter:
                if not self.rating_literary_works.check_udata(name):
                    return liter.response
                else:
                    # Удаляем старые оценки перед обновлением
                    self.rating_literary_works.rating_literary_works.delete_ratings_by_work_id(liter.id)

                    # Обновим существующий ответ
                    response = llm_client.send(name)
                    self.literary_repo.update_response(liter.id, response, llm=defoult_llm)
                    return response

            # Если произведения нет в базе — создаём
            response = llm_client.send(name)
            self.literary_repo.create(name, response, llm=defoult_llm)
            return response

        except Exception as e:
            raise Exception(f"Ошибка при обработке литературного произведения: {str(e)}")

    def get_list_response(self, page: int = 1, per_page: int = 10):
        try:
            total_items = self.literary_repo.count()
            total_pages = (total_items + per_page - 1) // per_page

            literary_works = self.literary_repo.get_paginated_list(page, per_page)
            return literary_works, total_pages
        except Exception as e:
            raise Exception(f"Ошибка при получении списка произведений: {str(e)}")
