from functools import wraps

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.connect import get_session
from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService


def check_blocked():
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            telegram_id = str(update.effective_user.id)

            session = get_session()
            users_repository = UsersRepository(session)  # Создаем экземпляр репозитория
            users_service = UsersService(users_repository)  # Передаем экземпляр в сервис

            user = users_service.is_user_blocked(telegram_id)
            if user:
                await update.message.reply_text(
                    "похоже, что вы заблокированы :-(",
                    parse_mode=ParseMode.MARKDOWN
                )
                return  # не продолжаем выполнение команды
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator
