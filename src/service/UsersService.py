from src.db.connect import get_session
from src.db.repository import UsersRepository


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo = users_repo(get_session())

    def check_registr(self, telegram_id: str) -> bool:
        """
        Проверяет, зарегистрирован ли пользователь
        
        Args:
            telegram_id (str): ID пользователя в Telegram
            
        Returns:
            bool: True если пользователь зарегистрирован, False в противном случае
        """
        try:
            user = self.users_repo.get_by_telegram_id(telegram_id)
            return user is not None
        except Exception as e:
            print(f"Ошибка при проверке регистрации пользователя: {str(e)}")
            return False

    def register(self, telegram_id: str, user_name: str, email: str):
        """
        Регистрирует нового пользователя или возвращает существующего
        
        Args:
            telegram_id (str): ID пользователя в Telegram
            user_name (str): Имя пользователя
            email (str): Email пользователя
            
        Returns:
            User: Объект пользователя
        """
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
