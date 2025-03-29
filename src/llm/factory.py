from src.llm.abstract_llm import LLMClient
from src.llm.constant import defoult_llm
from src.llm.giga_chat import GigaClient


class LlmFactory:
    @staticmethod
    def create(llm_type) -> LLMClient:
        if llm_type == "giga":
            return GigaClient()
        else:
            raise ValueError("тип llm не найден")


llm_client = LlmFactory.create(defoult_llm)
