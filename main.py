from src.db.connect import init_db
from src.telegram.bot import bot

if __name__ == "__main__":
    # Инициализируем базу данных
    init_db()
    # Запускаем бота
    bot()
