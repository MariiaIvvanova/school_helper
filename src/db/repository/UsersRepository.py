from datetime import datetime

from src.db.model.Users import Users
from src.db.model.constants import UserRole


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
            role="basic",
            create_date=now_date,
            updata_date=now_date
        )
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_by_telegram_id(self, telegram_id: str) -> Users:
        # Получает пользователя по telegram_id
        return self.session.query(Users).filter(Users.id == telegram_id).first()

    def get_by_user_name(self, user_name: str) -> Users:
        return self.session.query(Users).filter(Users.user_name == user_name).first()

    def set_block(self, user: Users, is_block: bool) -> bool:
        try:
            self.session.query(Users).filter(Users.id == user.id).update({"is_block": is_block})
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка при установке блокировки: {str(e)}")
            return False

    def check_block(self, telegram_id: str) -> bool:
        user = self.session.query(Users).filter(Users.id == telegram_id).first()
        if user:
            return user.is_block
        return False

    def check_role(self, telegram_id: str) -> str | None:
        user = self.session.query(Users).filter(Users.id == telegram_id).first()
        if user:
            return user.role
        return None

    def set_role(self, telegram_id: str, role: str) -> bool:
        if role not in UserRole.list():
            return False  # Нельзя назначать произвольную роль

        updated = self.session.query(Users).filter(Users.id == telegram_id).update({"role": role})
        self.session.commit()
        return bool(updated)
