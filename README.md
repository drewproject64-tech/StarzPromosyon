# Starz Promosyon

Telegram-native promotion information bot built with Python 3.12 and aiogram 3.x.

## Core functions

The bot deliberately has exactly three meaningful user-facing functions:

1. Promotions — browse three complete in-app promotion information items.
2. Updates — read three in-app Starz updates.
3. Submit Promotion — send promotion text, validate it, save it to SQLite, and receive a reference number.

There are no external website redirects in the user flow.

## Commands

- /start — resets the conversation and opens the main menu.
- /help — explains the three functions and navigation.

The bot also handles a Telegram Ads start parameter safely because /start is registered with aiogram's CommandStart filter.

## Configuration

Required: BOT_TOKEN=your_telegram_bot_token_here

Optional: ADMIN_ID=optional_numeric_telegram_user_id
DATABASE_PATH=starz_promosyon.db

Never commit real credentials.

## Local run

python -m venv .venv
pip install -r requirements.txt
python -m app.main

## Test

pip install -r requirements.txt
pytest -q

## Render

This repository uses a Render Background Worker.

Build command: pip install -r requirements.txt
Start command: python -m app.main

Set BOT_TOKEN in Render. If you want submission notifications, also set ADMIN_ID.

SQLite submissions are stored at DATABASE_PATH. The included Render configuration mounts a 1 GB persistent disk at /data and uses /data/starz_promosyon.db.

## QA checklist

Before advertising, verify on the live bot:

- /start
- /start campaign123
- /help
- Promotions → every item
- Updates → every item
- Submit Promotion → valid input
- Submit Promotion → empty/non-text input
- Submit Promotion → over 1,000 characters
- Run Again
- Main Menu
- repeated navigation
- malformed callback data
- restart and database initialization

The user-facing flow does not depend on an external website. Advertise only claims that accurately match these three functions.
