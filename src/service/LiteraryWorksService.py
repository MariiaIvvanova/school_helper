from src.db.connect import session
from src.db.repository import LiteraryWorksRepository
from src.llm.constant import defoult_llm
from src.llm.factory import llm_client


class LiteraryWorksService:
    def __init__(self, literary_repo: LiteraryWorksRepository):
        self.literary_repo = literary_repo(session)
        
    def upsert_literary(self, name) -> str:
        liter = self.literary_repo.get_by_name(name)
        if liter:
            return liter.response
        else:
            response = llm_client.send(name)
            self.literary_repo.create(name, response, llm=defoult_llm)
            return response

    def get_list_response(self, page=1, per_page=10):
        total_items = self.literary_repo.count()  # Количество всех записей
        total_pages = (total_items + per_page - 1) // per_page  # Округляем вверх

        # Получаем нужный диапазон записей
        literary_works = self.literary_repo.get_paginated_list(page, per_page)

        return literary_works, total_pages
