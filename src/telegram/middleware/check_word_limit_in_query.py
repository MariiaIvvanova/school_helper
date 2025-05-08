from telegram import Update
from telegram.constants import ParseMode

from functools import wraps


def check_word_limit_in_query(func):
    @wraps(func)
    async def wrapper(update: Update, *args, **kwargs):
        message = update.message.text.strip()  # Получаем текст сообщения

        # Проверка на количество слов и длину текста
        if len(message.split()) > 7 or len(message) > 60:
            await update.message.reply_text(
                "❗ Слишком много слов. Введите название литературного произведения (до 7 слов).",
                parse_mode=ParseMode.MARKDOWN
            )
            return  # Если ограничение нарушено, не выполняем основную функцию
        return await func(update, *args, **kwargs)  # Выполняем основную функцию, если условие прошло
    return wrapper
