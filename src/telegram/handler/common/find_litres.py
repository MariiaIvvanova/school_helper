from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.db.model.constants import UserRole
from src.db.repository.LiteraryWorksRepository import LiteraryWorksRepository
from src.db.repository.RatingLiteraryWorksRepository import RatingLiteraryWorksRepository
from src.db.repository import UsersRepository
from src.service.LiteraryWorksService import LiteraryWorksService
from src.service.RatingLiteraryWorksService import RatingLiteraryWorksService
from src.telegram.keyboard.rating_keyboard import get_rating_keyboard
from src.telegram.middleware.check_block import check_blocked
from src.telegram.middleware.check_message import check_message_not_empty
from src.telegram.middleware.check_register import check_register
from src.telegram.middleware.check_role import check_role
from src.telegram.middleware.check_word_limit_in_query import check_word_limit_in_query


from src.db.connect import get_session

@check_blocked()
@check_register()
# @check_role([UserRole.ADMIN])
@check_word_limit_in_query
@check_message_not_empty
async def find_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = " ".join(update.message.text.replace("/find", "").lower().split())

    session = get_session()
    literary_repo = LiteraryWorksRepository(session)
    rating_repo = RatingLiteraryWorksRepository(session)

    rating_service = RatingLiteraryWorksService(rating_repo, literary_repo)
    literary_works_service = LiteraryWorksService(literary_repo, rating_service, rating_repo)

    res = literary_works_service.upsert_literary(message)

    reply_markup = get_rating_keyboard(message)
    await update.message.reply_text(res, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

