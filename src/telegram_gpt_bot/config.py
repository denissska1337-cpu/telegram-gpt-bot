import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    openai_api_key: str
    openai_model: str


def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini"

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is not set in .env")

    return Settings(
        telegram_bot_token=token,
        openai_api_key=key,
        openai_model=model,
    )
