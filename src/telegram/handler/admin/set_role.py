from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from src.db.model.constants import UserRole
from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService
from src.telegram.middleware.check_block import check_blocked
from src.telegram.middleware.check_message import check_message_not_empty
from src.telegram.middleware.check_register import check_register
from src.telegram.middleware.check_role import check_role
from src.db.connect import get_session


@check_blocked()
@check_register()
@check_role([UserRole.ADMIN])
@check_message_not_empty
async def set_role_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = update.message.text.replace("/set_role", "").strip().split()
    user_name = " ".join(args)

    session = get_session()
    user_repo = UsersRepository(session)
    users_service = UsersService(user_repo)

    user = user_repo.get_by_user_name(user_name)
    if not user:
        await update.message.reply_text(f"❌ Пользователь '{user_name}' не найден.")
        return

    keyboard = [
        [InlineKeyboardButton(role, callback_data=f"setrole:{user.id}:{role}")]
        for role in UserRole.list()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Выберите роль для пользователя {user_name}:", reply_markup=reply_markup
    )
