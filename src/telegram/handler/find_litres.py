from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.service.LiteraryWorksService import LiteraryWorksService
from src.telegram.middleware.is_block import check_blocked
from src.telegram.middleware.is_message import check_message_not_empty
from src.telegram.middleware.is_register import check_register
from src.telegram.middleware.word_limit_in_query import word_limit_in_query


@check_blocked()
@check_register()
@word_limit_in_query
@check_message_not_empty
async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Обработка команды /find
    message = " ".join(update.message.text.replace("/find", "").lower().split())

    literary_works_service = LiteraryWorksService(LiteraryWorksRepository)
    res = literary_works_service.upsert_literary(message)

    await update.message.reply_text(res, parse_mode=ParseMode.MARKDOWN)
