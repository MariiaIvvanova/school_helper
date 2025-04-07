from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from src.config import config
from src.llm.constant import system_promt
from src.llm.factory import LLMClient


class GigaClient(LLMClient):
    def __init__(self):
        self.giga = GigaChat(
            credentials=config.GIGA_CHAT_AUTH_KEY,
            verify_ssl_certs=False,  # ⚠️ Не рекомендуется отключать SSL в проде
        )
        self.system_message = SystemMessage(content=system_promt)

    def send(self, prompt: str) -> str:
        messages = [
            self.system_message,
            HumanMessage(content=prompt),
        ]
        response = self.giga.invoke(messages)
        return response.content
