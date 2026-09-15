import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from app.config import Settings
from app.keyboards import back_menu, main_menu, promotion_menu

logging.basicConfig(level=logging.INFO)


def home_text() -> str:
    return (
        "🌟 <b>Starz Promosyon</b>\n\n"
        "A simple promotion hub for discovering campaigns and promotional opportunities.\n\n"
        "Choose an option below to explore the available information."
    )


def promotion_text() -> str:
    return (
        "📢 <b>Promotions</b>\n\n"
        "Explore the promotional options currently available through Starz Promosyon.\n\n"
        "Select the example below to see how a campaign can be presented."
    )


def example_text() -> str:
    return (
        "📋 <b>Example Promotion</b>\n\n"
        "Campaign: Starz Promosyon Showcase\n"
        "Goal: Introduce users to a promotional campaign and its details.\n"
        "Status: Example campaign\n\n"
        "This example demonstrates the bot's promotion-information flow."
    )


def about_text() -> str:
    return (
        "ℹ️ <b>About Starz Promosyon</b>\n\n"
        "Starz Promosyon provides a simple Telegram interface for viewing promotion information and example campaigns.\n\n"
        "Use the menu to explore the available sections."
    )


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message) -> None:
        await message.answer(home_text(), reply_markup=main_menu(), parse_mode="HTML")

    @dp.callback_query(F.data == "promotions")
    async def promotions(callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            promotion_text(), reply_markup=promotion_menu(), parse_mode="HTML"
        )
        await callback.answer()

    @dp.callback_query(F.data == "example_promotion")
    async def example_promotion(callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            example_text(), reply_markup=back_menu(), parse_mode="HTML"
        )
        await callback.answer()

    @dp.callback_query(F.data == "about")
    async def about(callback: CallbackQuery) -> None:
        await callback.message.edit_text(
            about_text(), reply_markup=back_menu(), parse_mode="HTML"
        )
        await callback.answer()

    @dp.callback_query(F.data == "back_home")
    async def back_home(callback: CallbackQuery) -> None:
        await callback.message.edit_text(home_text(), reply_markup=main_menu(), parse_mode="HTML")
        await callback.answer()

    return dp


async def main() -> None:
    settings = Settings.from_env()
    bot = Bot(token=settings.bot_token)
    dp = build_dispatcher()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
