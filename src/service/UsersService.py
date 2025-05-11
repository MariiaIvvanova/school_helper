from src.db.model.constants import UserRole
from src.db.repository import UsersRepository


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo

    def check_registr(self, telegram_id: str) -> bool:
        try:
            user = self.users_repo.get_by_telegram_id(telegram_id)
            return user is not None
        except Exception as e:
            print(f"Ошибка при проверке регистрации пользователя: {str(e)}")
            return False

    def register(self, telegram_id: str, user_name: str, email: str):
        try:
            user = self.users_repo.get_by_telegram_id(telegram_id)
            if user:
                return user
            else:
                self.users_repo.create(telegram_id, user_name, email)
                return self.users_repo.get_by_telegram_id(telegram_id)
        except Exception as e:
            print(f"Ошибка при регистрации пользователя: {str(e)}")
            return None

    def is_user_blocked(self, id: str) -> bool:
        try:
            return self.users_repo.check_block(id)
        except Exception as e:
            print(f"Ошибка при проверке блокировки пользователя: {str(e)}")
            return False

    def block_user(self, user_name: str, block: bool) -> bool:
        try:
            user = self.users_repo.get_by_user_name(user_name)
            if not user:
                print(f"Пользователь {user_name} не найден")
                return False
            return self.users_repo.set_block(user, block)
        except Exception as e:
            print(f"Ошибка при блокировке пользователя: {str(e)}")
            return False


    def check_role(self, telegram_id: str) -> str | None:
        try:
            return self.users_repo.check_role(telegram_id)
        except Exception as e:
            print(f"Ошибка при проверке роли пользователя: {str(e)}")
            return None

    def set_role(self, telegram_id: str, role: str) -> bool:
        try:
            if role not in UserRole.list():
                print(f"Попытка установить недопустимую роль: {role}")
                return False
            return self.users_repo.set_role(telegram_id, role)
        except Exception as e:
            print(f"Ошибка при установке роли: {str(e)}")
            return False
