from telegram import Update
from telegram.ext import CallbackContext

from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService
from src.db.connect import get_session


async def set_role_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    try:
        _, telegram_id, role = query.data.split(":")

        session = get_session()
        user_repo = UsersRepository(session)
        users_service = UsersService(user_repo)

        if users_service.set_role(telegram_id, role):
            await query.edit_message_text(f"✅ Роль '{role}' успешно назначена пользователю.")
        else:
            await query.edit_message_text(f"❌ Не удалось назначить роль '{role}'.")
    except Exception as e:
        await query.edit_message_text(f"❌ Ошибка: {e}")