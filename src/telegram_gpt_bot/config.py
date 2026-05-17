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
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set (Render Environment or .env)"
        )
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set (Render Environment or .env)"
        )

    return Settings(
        telegram_bot_token=token,
        openai_api_key=key,
        openai_model=model,
    )


def load_webhook_url() -> str:
    url = os.getenv("WEBHOOK_URL", "").strip()
    if not url:
        raise RuntimeError(
            "WEBHOOK_URL is not set (Render Environment or .env), "
            "e.g. https://your-app.onrender.com/webhook"
        )
    return url
