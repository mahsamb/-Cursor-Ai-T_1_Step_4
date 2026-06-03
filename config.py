import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///shop.db")
    admin_ids_raw: str = os.getenv("ADMIN_IDS", "")

    @property
    def admin_ids(self) -> set[int]:
        if not self.admin_ids_raw.strip():
            return set()
        return {int(item.strip()) for item in self.admin_ids_raw.split(",") if item.strip()}


settings = Settings()
