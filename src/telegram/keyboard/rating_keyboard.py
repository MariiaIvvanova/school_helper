from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_rating_keyboard(work_title: str) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("👍", callback_data=f"like|{work_title}"),
            InlineKeyboardButton("👎", callback_data=f"dislike|{work_title}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
