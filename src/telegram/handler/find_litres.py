from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.db.repository.UsersRepository import UsersRepository
from src.service.LiteraryWorksService import LiteraryWorksService
from src.service.UsersService import UsersService
from src.telegram.middleware.block import block
from src.telegram.middleware.word_limit_in_query import word_limit_in_query


async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверка на наличие текста
    if not update.message or not update.message.text:
        await update.effective_chat.send_message("Команда должна быть отправлена в виде текстового сообщения.")
        return

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

    # Проверка блокировки
    is_blocked = await block(update, context)
    if is_blocked:
        return

    # Обработка команды /find
    message = " ".join(update.message.text.replace("/find", "").lower().split())

    if not await word_limit_in_query(update, message):
        return
    if not message:
        await update.message.reply_text("Вы ничего не написали")
        return

    literary_works_service = LiteraryWorksService(LiteraryWorksRepository)
    res = literary_works_service.upsert_literary(message)

    await update.message.reply_text(res, parse_mode=ParseMode.MARKDOWN)
