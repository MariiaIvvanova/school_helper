from src.db.connect import session
from src.db.repository import UsersRepository


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo(session)

    def register(self, telegram_id, user_name, email):
        user = self.users_repo.get_by_telegram_id(telegram_id)
        if user:
            return user
        else:
            user = self.users_repo.create(telegram_id, user_name, email)
            return user
