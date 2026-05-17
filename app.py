import os
import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from telegram_gpt_bot.app import run_polling


def _render_port() -> int:
    return int(os.environ.get("PORT", "8000"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    thread = threading.Thread(target=run_polling, name="telegram-polling", daemon=True)
    thread.start()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=_render_port())


if __name__ == "__main__":
    main()
