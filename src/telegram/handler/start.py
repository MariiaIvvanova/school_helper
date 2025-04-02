from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService

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


# Обработчик команды /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, не ожидаем ли мы уже email
    if context.user_data.get('awaiting_email'):
        await update.message.reply_text(
            "Пожалуйста, сначала введите ваш email адрес.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    users_service = UsersService(UsersRepository)
    user = users_service.check_registr(update.effective_user.id)
    
    if user:
        await update.message.reply_text(message, parse_mode=ParseMode.MARKDOWN)
    else:
        # Запрашиваем email у пользователя
        await update.message.reply_text(
            "Для начала работы, пожалуйста, отправьте свой email адрес.",
            parse_mode=ParseMode.MARKDOWN
        )
        # Сохраняем состояние ожидания email
        context.user_data['awaiting_email'] = True


#
# UsersService.check_users
# if users
#     print(start)
# else
#     print("введите почту")
#     UsersService.registr()
#     print(start)


