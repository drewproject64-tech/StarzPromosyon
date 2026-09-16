# Starz Promosyon

Starz Promosyon is a Telegram-native promotion information bot built with Python 3.12 and aiogram 3.x.

## Exactly three user functions

1. Promotions — browse promotion information shown directly in Telegram.
2. Updates — read Starz Promosyon updates directly in Telegram.
3. Submit Promotion — submit promotion text, validate it, save it to SQLite and receive a reference number.

The user experience does not depend on an external website or redirect.

## Commands

- /start — opens the main menu and safely accepts Telegram deep-link start parameters.
- /help — explains the three functions and navigation.

All other user interaction is through the inline keyboard.

## Configuration

Required: BOT_TOKEN=your_telegram_bot_token_here
Optional: ADMIN_ID=optional_numeric_telegram_user_id
Optional: DATABASE_PATH=data/starz_promosyon.db

No secrets are stored in the repository.

## Local run

    python -m venv .venv
    pip install -r requirements.txt
    python -m app.main

## Tests

    pytest -q

The test suite covers the content contract, callback index validation, SQLite initialization/submission and dispatcher construction.

## Render

This repository uses a Render Background Worker.

- Build: pip install -r requirements.txt
- Start: python -m app.main
- Required environment variable: BOT_TOKEN
- Optional: ADMIN_ID
- Database: /data/starz_promosyon.db in the included Render persistent disk configuration
- Polling is used and any existing webhook is removed at startup.

## Production QA

Before advertising, verify the live bot manually:

1. /start
2. /start campaign123
3. /help
4. Promotions → each item → Back → Main Menu
5. Updates → each item → Back → Main Menu
6. Submit Promotion → valid text → reference → Run Again
7. Submit Promotion → empty/non-text input
8. Submit Promotion → more than 1,000 characters
9. Malformed callback data
10. Repeated navigation
11. Restart and database initialization

Replace the example promotion/update copy with real, current content before using the bot commercially. Do not advertise claims the bot does not actually provide.

## Telegram Ads notes

Telegram's current Ads guidelines require destination bots to be functional, technically complete and active, to respond properly to commands on mobile and desktop, and not to be used primarily as redirects. They also require a complete bot profile with a profile image and description. The ad and destination must accurately match.

Source: https://ads.telegram.org/guidelines