# Starz Promosyon

A lightweight Telegram promotion-information bot built with Python and aiogram 3.x.

## Features

- `/start` welcome flow
- Inline menu navigation
- Promotions section
- Functional example promotion
- About section
- Environment-variable configuration
- Render worker deployment configuration

## Environment variables

```text
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=optional_numeric_telegram_user_id
```

`BOT_TOKEN` is required. Do not commit secrets to the repository.

## Local run

```bash
pip install -r requirements.txt
python -m app.main
```

## Deploy on Render

Use the included `render.yaml` or create a Python Background Worker with:

- Build command: `pip install -r requirements.txt`
- Start command: `python -m app.main`

Set `BOT_TOKEN` in Render environment variables.
