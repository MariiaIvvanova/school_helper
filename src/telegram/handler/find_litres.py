from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.service.LiteraryWorksService import LiteraryWorksService


async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text.replace("/find", "")
    if not message:
        await update.message.reply_text("Вы ничего не написали")
        return

    literary_works_service = LiteraryWorksService(LiteraryWorksRepository)
    res = literary_works_service.upsert_literary(message)

    await update.message.reply_text(res, parse_mode=ParseMode.MARKDOWN)
