from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    turkeysms_api_key: str
    turkeysms_sender: str
    database_url: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
    )


settings = Settings()