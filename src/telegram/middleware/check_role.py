from functools import wraps
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from typing import Callable

from src.db.connect import get_session
from src.db.model.constants import UserRole
from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService


def check_role(allowed_roles: list[UserRole]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            telegram_id = str(update.effective_user.id)

            session = get_session()
            users_repository = UsersRepository(session)  # Создаем экземпляр репозитория
            users_service = UsersService(users_repository)

            user_role = users_service.check_role(telegram_id)

            if user_role not in [role.value for role in allowed_roles]:
                await update.message.reply_text(
                    "⛔ У вас нет доступа к этой команде.",
                    parse_mode=ParseMode.MARKDOWN
                )
                return

            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator
