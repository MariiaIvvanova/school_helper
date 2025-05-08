from functools import wraps
from telegram import Update


def check_message_not_empty(func):
    @wraps(func)
    async def wrapper(update: Update, *args, **kwargs):
        message = " ".join(update.message.text.replace("/find", "").replace("/set_block", "").lower().split())

        if not message:
            await update.message.reply_text("Вы ничего не написали")
            return
        return await func(update, *args, **kwargs)

    return wrapper
