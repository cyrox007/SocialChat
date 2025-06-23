import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Секретный ключ
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key-for-development")

    # Путь к проекту
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Конфигурация базы данных
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "chat")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    def database_url(self, async_mode=False):
        driver = "postgresql+asyncpg" if async_mode else "postgresql"
        return f"{driver}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Настройки аватаров
    FULL_AVATARS_PATH = os.path.join(BASE_DIR, 'static', 'uploads', 'us_avatars')
    AVATAR_DIR = 'uploads/us_avatars/'


config = Config()