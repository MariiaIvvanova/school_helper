from datetime import datetime

from src.db.model.Users import Users


class UsersRepository:
    def __init__(self, session):
        self.session = session

    def create(self, telegram_id: str, user_name: str, email: str) -> Users:
        # Создает нового пользователя
        now = datetime.now()
        now_date = now.isoformat(timespec='milliseconds')
        new_user = Users(
            id=telegram_id,
            user_name=user_name,
            email=email,
            is_block=False,
            create_date=now_date,
            updata_date=now_date
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_by_telegram_id(self, telegram_id: str) -> Users:
        # Получает пользователя по telegram_id
        return self.session.query(Users).filter(Users.id == telegram_id).first()

    def set_block(self, telegram_id: str, is_block: bool) -> None:
        # Устанавливает статус блокировки пользователя
        self.session.query(Users).filter(Users.id == telegram_id).update({"is_block": is_block})
        self.session.commit()

    def check_block(self, telegram_id: str) -> bool:
        user = self.session.query(Users).filter(Users.id == telegram_id).first()
        if user:
            return user.is_block
        return False
