from functools import wraps

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService


def check_register():
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            telegram_id = str(update.effective_user.id)
            users_service = UsersService(UsersRepository)

            # Проверка регистрации
            user = users_service.check_registr(telegram_id)
            if not user:
                context.user_data['awaiting_email'] = True
                await update.message.reply_text(
                    "Похоже, вы ещё не зарегистрированы.\n"
                    "Пожалуйста, введите ваш email для регистрации:",
                    parse_mode=ParseMode.MARKDOWN
                )
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator
