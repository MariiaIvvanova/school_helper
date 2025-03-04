from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat

from src.config import Config

config = Config()
giga = GigaChat(
    # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
    credentials=config.GIGA_CHAT_AUTH_KEY,
    verify_ssl_certs=False,
)

messages = [
    SystemMessage(
        content="""Ты — интеллектуальный литературный справочник. Пользователь вводит название книги, а ты предоставляешь информацию в следующем формате:
 1. Название: [Оригинальное название + год публикации]
 2. Автор: [ФИО автора и краткая биография]
 3. Жанр: [Роман, философская литература, фантастика и т. д.]
 4. Краткое описание: [2-3 предложения о сюжете]
 5. Краткое содержание: [Основные события книги в сжатом виде 10 предложений]
 6. Философские вопросы:
 • Какое главное послание этой книги?
 • Какие моральные или этические вопросы она поднимает?
 • Какую идею автор хотел донести до читателя?"""
    )
]

while True:
    user_input = input("Пользователь: ")
    if user_input == "пока":
      break
    messages.append(HumanMessage(content=user_input))
    res = giga.invoke(messages)
    messages.append(res)
    print("GigaChat: ", res.content)