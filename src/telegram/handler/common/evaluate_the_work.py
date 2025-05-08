from telegram import Update
from telegram.ext import ContextTypes


async def rating_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, work_title = query.data.split("|", 1)
    telegram_id = str(query.from_user.id)

    rating = 1 if action == "like" else 0
    context.application.rating_service.add_rating(telegram_id, work_title, rating)

    await query.edit_message_reply_markup(reply_markup=None)
    await query.message.reply_text("Вы поставили 👍" if rating == 1 else "Вы поставили 👎")
