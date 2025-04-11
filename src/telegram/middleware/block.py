from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService


async def block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    telegram_id = str(update.effective_user.id)
    users_service = UsersService(UsersRepository)


    user = users_service.is_user_blocked(telegram_id)
    if user:
        await update.message.reply_text(
            "похоже, что вы заблокированы :-(",
            parse_mode=ParseMode.MARKDOWN
        )
        return True  # пользователь заблокирован
    return False