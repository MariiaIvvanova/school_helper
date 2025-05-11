from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.connect import get_session
from src.db.repository.UsersRepository import UsersRepository
from src.service.UsersService import UsersService

async def handle_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get('awaiting_email'):
        return

    email = update.message.text.strip()
    
    # Простая валидация email
    if '@' not in email or '.' not in email:
        await update.message.reply_text(
            "Пожалуйста, введите корректный email адрес.",
            parse_mode=ParseMode.MARKDOWN
        )
        return

    try:
        session = get_session()
        users_repository = UsersRepository(session)
        users_service = UsersService(users_repository)
        user = users_service.register(
            telegram_id=str(update.effective_user.id),
            user_name=update.effective_user.username or "Unknown",
            email=email
        )
        
        if user:
            context.user_data.pop('awaiting_email', None)
            
            await update.message.reply_text(
                "Спасибо за регистрацию! Теперь вы можете использовать бота.\n"
                "Используйте команду /find для поиска информации о книгах.",
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                "Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.",
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        await update.message.reply_text(
            "Произошла ошибка при обработке email. Пожалуйста, попробуйте позже.",
            parse_mode=ParseMode.MARKDOWN
        )
