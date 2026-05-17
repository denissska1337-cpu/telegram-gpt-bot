from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from telegram_gpt_bot.config import load_settings
from telegram_gpt_bot.handlers import on_text_message


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


def run_polling() -> None:
    app = build_application()
    app.run_polling(allowed_updates=["message"])
