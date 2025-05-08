from datetime import datetime

from telegram import Update
from telegram.constants import ParseMode
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
async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = " ".join(update.message.text.replace("/set_block", "").split()).strip()

    session = get_session()
    user_repo = UsersRepository(session)
    users_service = UsersService(user_repo)

    user = user_repo.get_by_user_name(user_name)
    if not user:
        await update.message.reply_text(
            f"❌ Пользователь <b>{user_name}</b> не найден в системе\n\n"
            "Проверьте правильность имени и повторите попытку"
        )
        return

    if user.is_block:
        result = users_service.block_user(user_name, False)
        if result:
            await update.message.reply_text(
                f"⚠️ Пользователь разблокирован\n\n"
                f"👤 <b>{user_name}</b>\n"
                f"🆔 ID: <code>{user.id}</code>\n"
                f"📅 Дата регистрации: {user.create_date.strftime('%d.%m.%Y %H:%M')}\n"
                f"⏱ Дата разблокировки: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
        else:
            await update.message.reply_text(
                f"❌ Не удалось разблокировать пользователя <b>{user_name}</b>\n\n"
                "Попробуйте позже или обратитесь к разработчику"
            )
        return

    else:
        result = users_service.block_user(user_name, True)
        if result:
            await update.message.reply_text(
                f"✅ Пользователь успешно заблокирован\n\n"
                f"👤 <b>{user_name}</b>\n"
                f"🆔 ID: <code>{user.id}</code>\n"
                f"📅 Дата регистрации: {user.create_date.strftime('%d.%m.%Y %H:%M')}\n"
                f"⏱ Дата блокировки: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            )
        else:
            await update.message.reply_text(
                f"❌ Не удалось заблокировать пользователя <b>{user_name}</b>\n\n"
                "Попробуйте позже или обратитесь к разработчику"
            )
        return
