import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from src.config import Config
from src.llm.giga_chat import giga

config = Config()
TOKEN = config.TG_BOT_KEY

# Включаем логгирование для удобства отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text("Привет! Я бот. Чем могу помочь?")
    # print(update.message.text, update.message.from_user.username)
    message = update.message.text.replace("/start ", "")
    res = giga.invoke(message)
    await update.message.reply_text(res.content)


def main():
    # Создаём приложение (Application) с указанным токеном
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start_command))

    # Запускаем бота в режиме "polling" — бот будет регулярно опрашивать сервер Telegram
    application.run_polling()

if __name__ == "__main__":
    main()