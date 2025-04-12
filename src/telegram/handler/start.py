from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.telegram.middleware.is_block import check_blocked

message = """📖 Telegram-бот "Литературный справочник"

📌 Описание бота
Бот предназначен для быстрого поиска информации о книгах. Он использует возможности ChatGPT, чтобы предоставить развернутый ответ по заданному произведению в структурированном формате.

🔧 Как пользоваться
Откройте чат с ботом в Telegram.

/find [название книги]

Например:
/find Преступление и наказание

Бот обработает запрос и отправит информацию о книге в следующем формате:
```
Название: Оригинальное название + год публикации
Автор: ФИО автора и краткая биография
Жанр: Литературное направление
Краткое описание: 2–3 предложения о сюжете
Краткое содержание: Основные события в 10 предложениях
Философские вопросы: Темы и идеи, которые поднимает книга
```
"""

@check_blocked()    # Проверка блокировки
# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
