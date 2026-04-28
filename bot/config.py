from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    bot_token: str
    db_path: str = "shopping_bot.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

config = Settings()