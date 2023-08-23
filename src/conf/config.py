from pydantic_settings import BaseSettings
from pathlib import Path

CURRENT_URL = Path(__file__).resolve().parent
BASE_URL = CURRENT_URL.parent


class Settings(BaseSettings):
    DEBUG: bool = True
    API_V1_STR: str = ""
    DB_NAME: str = "db.sqlite3"
    DB_URI: str = f"sqlite+aiosqlite:///{BASE_URL / DB_NAME}"
    TEST_DB_URI: str = f"sqlite+aiosqlite:///{BASE_URL / 'test.sqlite3'}"
    DB_MIGRATIONS_URI: str = f"sqlite:///{BASE_URL / DB_NAME}"

    class Config:
        env_file = '.env'


settings = Settings()