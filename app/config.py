from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator


class Settings(BaseSettings):
    bot_token: SecretStr
    gemini_api_key: SecretStr | None = None
    groq_api_key: SecretStr | None = None
    admin_chat_id: int | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, v: SecretStr) -> SecretStr:
        value = v.get_secret_value()
        if not value or value == "...":
            raise ValueError("BOT_TOKEN not configured in .env")
        return v


config = Settings()