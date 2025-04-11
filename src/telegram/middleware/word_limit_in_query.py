from telegram import Update
from telegram.constants import ParseMode


async def word_limit_in_query(update: Update, message: str):
    text = message.strip()

    if len(text.split()) > 5 or len(text) > 50:
        await update.message.reply_text(
            "❗ Слишком много слов. Введите название литературного произведения (до 5 слов).",
            parse_mode=ParseMode.MARKDOWN
        )
        return False
    return True