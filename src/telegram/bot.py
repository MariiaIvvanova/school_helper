import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from src.config import config
from src.telegram.commands import FIND_COMMAND, START_COMMAND
from src.telegram.handler.find_litres import find_command
from src.telegram.handler.start import start_command
from src.telegram.handler.email import handle_email


TOKEN = config.TG_BOT_KEY

# Включаем логгирование для удобства отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)



def bot():
    # Создаём приложение (Application) с указанным токеном
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler(FIND_COMMAND, find_command))
    application.add_handler(CommandHandler(START_COMMAND, start_command))
    
    # Регистрируем обработчик для email
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_email))

    # Запускаем бота в режиме "polling" — бот будет регулярно опрашивать сервер Telegram
    application.run_polling()
