import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Включаем логгирование для удобства отладки
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Вставьте сюда ваш токен, полученный от BotFather
TOKEN = "7605076216:AAEputBeLuKhx41s_b77dwcUu6K1rlygxEU"

# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот. Чем могу помочь?")

def main():
    # Создаём приложение (Application) с указанным токеном
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start_command))

    # Запускаем бота в режиме "polling" — бот будет регулярно опрашивать сервер Telegram
    application.run_polling()

if __name__ == "__main__":
    main()