# Telegram GPT Bot

Телеграм-бот на [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v21, отвечает на текстовые сообщения через [OpenAI API](https://platform.openai.com/docs/overview).

## Структура проекта

```
telegram-gpt-bot/
├── app.py                  # FastAPI health + webhook (Render)
├── pyproject.toml          # метаданные пакета и зависимости
├── requirements.txt       # те же зависимости для классического pip install
├── .env.example             # шаблон переменных окружения
├── README.md
└── src/
    └── telegram_gpt_bot/
        ├── __init__.py
        ├── __main__.py      # точка входа: python -m telegram_gpt_bot
        ├── app.py           # сборка Application, webhook и polling
        ├── config.py        # загрузка .env и настройки
        ├── gpt.py           # вызов Chat Completions
        └── handlers.py      # обработчики сообщений
```

## Требования

- Python 3.11+
- Токен бота у [@BotFather](https://t.me/BotFather)
- Ключ API OpenAI с [платформы OpenAI](https://platform.openai.com/api-keys)

## Запуск

### 1. Клонирование и виртуальное окружение

```powershell
cd путь\к\telegram-gpt-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

В Linux или macOS:

```bash
cd /path/to/telegram-gpt-bot
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Установка зависимостей

**Рекомендуется** — editable-установка пакета из `src/` (подтянет зависимости из `pyproject.toml`):

```bash
pip install -e .
```

**Альтернатива** — только `requirements.txt`, тогда нужно указать путь к пакету:

```powershell
pip install -r requirements.txt
$env:PYTHONPATH = "src"
```

В bash:

```bash
pip install -r requirements.txt
export PYTHONPATH=src
```

### 3. Переменные окружения

Скопируйте шаблон и подставьте свои ключи:

```powershell
copy .env.example .env
```

Отредактируйте `.env`:

- `TELEGRAM_BOT_TOKEN` — токен от BotFather
- `OPENAI_API_KEY` — ключ OpenAI
- `OPENAI_MODEL` — необязательно, по умолчанию `gpt-4o-mini`
- `WEBHOOK_URL` — полный URL webhook для Render, например `https://telegram-gpt-bot.onrender.com/webhook` (нужен только для `app.py` / Render, не для локального polling)

Файл `.env` не коммитьте в git (он уже в `.gitignore`).

### 4. Запуск бота

**Локально (polling)** — без `WEBHOOK_URL`, удобно для разработки:

```bash
python -m telegram_gpt_bot
```

Перед первым polling на Render снимите webhook, если он был установлен: бот не должен работать в двух режимах одновременно с одним токеном.

**Render / production (webhook)** — через FastAPI, polling не используется:

```bash
python app.py
```

или `uvicorn app:app --host 0.0.0.0 --port $PORT`.

- `GET /` → `{"status":"ok"}`
- `POST /webhook` — обновления от Telegram

При старте `app.py` вызывается `bot.set_webhook` с URL из `WEBHOOK_URL`.

## Деплой на Render

1. **Build command:** `pip install -e .`
2. **Start command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
3. В **Environment** задайте:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (опционально)
   - `WEBHOOK_URL` — `https://<имя-сервиса>.onrender.com/webhook`

Render выставляет `PORT`; health check — `GET /`. Telegram шлёт обновления на `POST /webhook`.

## Примечания

- Обрабатываются только текстовые сообщения (не команды). Сообщения-команды вида `/help` игнорируются фильтром `~filters.COMMAND`.
- Длинные ответы обрезаются до 4096 символов (лимит одного сообщения в Telegram).
