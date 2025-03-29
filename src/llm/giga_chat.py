from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from src.config import Config
from src.llm.constant import system_promt
from src.llm.factory import LLMClient


class GigaClient(LLMClient):
    def __init__(self):
        config = Config()
        self.giga = GigaChat(
            credentials=config.GIGA_CHAT_AUTH_KEY,
            verify_ssl_certs=False,
        )
        messages = [
            SystemMessage(
                content=system_promt
            )
        ]

    def send(self, promt):
        res = self.giga.invoke(promt)
        return res.content
