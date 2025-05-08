import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from src.config import config
from src.db.connect import get_session
from src.telegram.commands import FIND_COMMAND, START_COMMAND, SET_BLOCK_COMMAND
from src.telegram.handler.common.evaluate_the_work import rating_button_handler
from src.telegram.handler.common.find_litres import find_command
from src.telegram.handler.admin.set_block import block_command
from src.telegram.handler.common.start import start_command
from src.telegram.handler.common.email import handle_email
from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.db.repository.RatingLiteraryWorksRepository import RatingLiteraryWorksRepository
from src.service.RatingLiteraryWorksService import RatingLiteraryWorksService


TOKEN = config.TG_BOT_KEY

# Включаем логгирование для удобства отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def bot():
    # создаём репозитории
    literary_repo = LiteraryWorksRepository(get_session())
    rating_repo = RatingLiteraryWorksRepository(get_session())

    # создаём сервис
    rating_service = RatingLiteraryWorksService(rating_repo, literary_repo)

    # создаём приложение
    application = ApplicationBuilder().token(TOKEN).build()

    # добавляем сервис в приложение
    application.rating_service = rating_service

    # обработчики
    application.add_handler(CommandHandler(FIND_COMMAND, find_command))
    application.add_handler(CommandHandler(START_COMMAND, start_command))
    application.add_handler(CommandHandler(SET_BLOCK_COMMAND, block_command))
    application.add_handler(CallbackQueryHandler(rating_button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))

    application.run_polling()
