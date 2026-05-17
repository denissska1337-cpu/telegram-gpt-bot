from openai import OpenAIError
from telegram import Update
from telegram.ext import ContextTypes

from telegram_gpt_bot.gpt import reply_text


async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    client = context.application.bot_data["openai_client"]
    model = context.application.bot_data["openai_model"]
    text = update.message.text

    thinking = await update.message.reply_text("…")
    try:
        answer = await reply_text(client, model, text)
        if not answer:
            answer = "Пустой ответ от модели."
        await thinking.edit_text(answer[:4096])
    except OpenAIError as exc:
        await thinking.edit_text(f"Ошибка OpenAI: {exc}")
