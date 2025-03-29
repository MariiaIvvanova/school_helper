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
