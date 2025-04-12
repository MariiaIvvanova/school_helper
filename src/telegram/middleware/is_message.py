from functools import wraps
from telegram import Update


def check_message_not_empty(func):
    @wraps(func)
    async def wrapper(update: Update, *args, **kwargs):
        message = " ".join(update.message.text.replace("/find", "").lower().split())

        if not message:
            await update.message.reply_text("Вы ничего не написали")
            return  # Если сообщение пустое, останавливаем выполнение функции
        return await func(update, *args, **kwargs)  # Иначе вызываем оригинальную функцию

    return wrapper
