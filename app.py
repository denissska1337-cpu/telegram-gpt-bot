import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
import uvicorn

from telegram_gpt_bot.app import (
    build_application,
    process_webhook_update,
    start_webhook,
    stop_webhook,
)
from telegram_gpt_bot.config import load_webhook_url

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _render_port() -> int:
    return int(os.environ.get("PORT", "8000"))


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    application = build_application()
    webhook_url = load_webhook_url()
    fastapi_app.state.ptb_application = application

    try:
        await start_webhook(application, webhook_url)
    except Exception:
        logger.exception("Failed to register Telegram webhook")
        raise

    try:
        yield
    finally:
        await stop_webhook(application)


app = FastAPI(lifespan=lifespan)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook")
async def webhook(request: Request) -> dict[str, bool]:
    application = request.app.state.ptb_application
    data = await request.json()
    await process_webhook_update(application, data)
    return {"ok": True}


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=_render_port())


if __name__ == "__main__":
    main()
