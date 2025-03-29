import os

from dotenv import load_dotenv


class Config:

    def __init__(self, env_file=".env"):
        self.env_file = env_file
        load_dotenv(self.env_file)
        required_env = ["TG_BOT_KEY", "GIGA_CHAT_AUTH_KEY", "DATABASE_URL"]
        missing_keys = [key for key in required_env if os.getenv(key) is None]
        if missing_keys:
            raise ValueError(
                f"Не найдены необходимые переменные окружения: {', '.join(missing_keys)}"
            )

        self.TG_BOT_KEY = os.getenv("TG_BOT_KEY")
        self.GIGA_CHAT_AUTH_KEY = os.getenv("GIGA_CHAT_AUTH_KEY")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
