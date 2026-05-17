import logging
from typing import Any

from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from telegram_gpt_bot.config import load_settings
from telegram_gpt_bot.handlers import on_text_message

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "Пришлите любое текстовое сообщение — отвечу через OpenAI."
        )


def build_application() -> Application:
    settings = load_settings()
    application = (
        Application.builder()
        .token(settings.telegram_bot_token)
        .build()
    )
    application.bot_data["openai_client"] = AsyncOpenAI(api_key=settings.openai_api_key)
    application.bot_data["openai_model"] = settings.openai_model

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, on_text_message)
    )
    return application


async def start_webhook(application: Application, webhook_url: str) -> None:
    await application.initialize()
    await application.start()
    await application.bot.set_webhook(
        url=webhook_url,
        allowed_updates=["message"],
    )
    logger.info("Webhook registered: %s", webhook_url)


async def stop_webhook(application: Application) -> None:
    await application.bot.delete_webhook()
    await application.stop()
    await application.shutdown()
    logger.info("Webhook removed")


async def process_webhook_update(application: Application, data: dict[str, Any]) -> None:
    update = Update.de_json(data, application.bot)
    if update is not None:
        await application.process_update(update)


def run_polling() -> None:
    """Локальный запуск: python -m telegram_gpt_bot (без Render / webhook)."""
    build_application().run_polling(allowed_updates=["message"])
