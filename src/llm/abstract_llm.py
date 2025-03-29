from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def send(self, prompt: str) -> str:
        pass
