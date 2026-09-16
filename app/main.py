from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from app.config import Settings
from app.content import PROMOTIONS, UPDATES
from app.keyboards import item_menu, main_menu, result_menu, submit_menu
from app.storage import Storage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("starz_promosyon")


class SubmitState(StatesGroup):
    waiting_for_text = State()


def home_text() -> str:
    return (
        "🌟 <b>Starz Promosyon</b>\n\n"
        "A Telegram-native promotion hub for browsing promotional information, "
        "reading in-app updates, and submitting a promotion for consideration.\n\n"
        "<b>Choose one of the 3 functions:</b>\n"
        "📢 Promotions — browse promotion information\n"
        "📰 Updates — read Starz updates\n"
        "✍️ Submit Promotion — send a promotion for review"
    )


def help_text() -> str:
    return (
        "ℹ️ <b>Help</b>\n\n"
        "Use the main menu to choose one of the three available functions.\n\n"
        "📢 <b>Promotions:</b> choose an item and read its details.\n"
        "📰 <b>Updates:</b> choose an update and read it in the chat.\n"
        "✍️ <b>Submit Promotion:</b> send clear promotion text and receive a reference number.\n\n"
        "Use <b>/start</b> or the Main Menu button at any time to return home."
    )


def list_text(title: str, items: tuple) -> str:
    lines = [f"<b>{title}</b>", "", "Choose an item to view its details:"]
    for index, item in enumerate(items, 1):
        lines.append(f"{index}. {item.title}")
    return "\n".join(lines)


def item_text(item, index: int, total: int) -> str:
    return f"<b>{item.title}</b>\n\n{item.body}\n\n<i>Item {index + 1} of {total}</i>"


def build_dispatcher(storage: Storage, settings: Settings) -> Dispatcher:
    dp = Dispatcher()

    @dp.message(CommandStart())
    async def start(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(home_text(), reply_markup=main_menu(), parse_mode="HTML")

    @dp.message(Command("help"))
    async def help_command(message: Message, state: FSMContext) -> None:
        await state.clear()
        await message.answer(help_text(), reply_markup=main_menu(), parse_mode="HTML")

    @dp.callback_query(F.data == "home")
    async def home(callback: CallbackQuery, state: FSMContext) -> None:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(home_text(), reply_markup=main_menu(), parse_mode="HTML")

    @dp.callback_query(F.data == "promotions")
    async def promotions(callback: CallbackQuery, state: FSMContext) -> None:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(
            list_text("📢 Promotions", PROMOTIONS),
            reply_markup=item_menu("promotion", len(PROMOTIONS)),
            parse_mode="HTML",
        )

    @dp.callback_query(F.data.startswith("promotion:"))
    async def promotion_item(callback: CallbackQuery) -> None:
        try:
            index = int(callback.data.split(":", 1)[1])
            item = PROMOTIONS[index]
        except (ValueError, IndexError, AttributeError):
            await callback.answer("That option is no longer available.", show_alert=True)
            return

        await callback.answer()
        await callback.message.edit_text(
            item_text(item, index, len(PROMOTIONS)),
            reply_markup=result_menu("promotions"),
            parse_mode="HTML",
        )

    @dp.callback_query(F.data == "updates")
    async def updates(callback: CallbackQuery, state: FSMContext) -> None:
        await state.clear()
        await callback.answer()
        await callback.message.edit_text(
            list_text("📰 Updates", UPDATES),
            reply_markup=item_menu("update", len(UPDATES)),
            parse_mode="HTML",
        )

    @dp.callback_query(F.data.startswith("update:"))
    async def update_item(callback: CallbackQuery) -> None:
        try:
            index = int(callback.data.split(":", 1)[1])
            item = UPDATES[index]
        except (ValueError, IndexError, AttributeError):
            await callback.answer("That option is no longer available.", show_alert=True)
            return

        await callback.answer()
        await callback.message.edit_text(
            item_text(item, index, len(UPDATES)),
            reply_markup=result_menu("updates"),
            parse_mode="HTML",
        )

    @dp.callback_query(F.data == "submit")
    async def submit(callback: CallbackQuery, state: FSMContext) -> None:
        await state.set_state(SubmitState.waiting_for_text)
        await callback.answer()
        await callback.message.edit_text(
            "✍️ <b>Submit Promotion</b>\n\n"
            "Send the promotion text you want to submit.\n\n"
            "Keep it clear and useful. Maximum length: 1,000 characters.\n"
            "Do not send passwords, payment credentials or other private information.",
            reply_markup=submit_menu(),
            parse_mode="HTML",
        )

    @dp.message(SubmitState.waiting_for_text)
    async def receive_submission(message: Message, state: FSMContext) -> None:
        text = (message.text or "").strip()

        if not text:
            await message.answer(
                "That input isn't valid. Please send text for the promotion.",
                reply_markup=submit_menu(),
            )
            return

        if len(text) > 1000:
            await message.answer(
                "Your promotion is too long. Please keep it to 1,000 characters or fewer.",
                reply_markup=submit_menu(),
            )
            return

        try:
            submission_id = storage.add_submission(
                user_id=message.from_user.id,
                username=message.from_user.username,
                text=text,
            )
        except Exception:
            logger.exception("Failed to save promotion submission")
            await message.answer(
                "We couldn't save that submission right now. Please try again.",
                reply_markup=submit_menu(),
            )
            return

        await state.clear()
        await message.answer(
            f"✅ <b>Submission received</b>\n\n"
            f"Reference: <code>SP-{submission_id:06d}</code>\n"
            "Your promotion has been saved for consideration.",
            reply_markup=result_menu("submit"),
            parse_mode="HTML",
        )

        if settings.admin_id:
            try:
                await message.bot.send_message(
                    settings.admin_id,
                    f"New Starz Promosyon submission SP-{submission_id:06d}\n"
                    f"User: {message.from_user.id}\n"
                    f"Text: {text}",
                )
            except TelegramAPIError:
                logger.exception("Failed to notify admin about submission")

    @dp.message()
    async def fallback(message: Message, state: FSMContext) -> None:
        if await state.get_state() == SubmitState.waiting_for_text:
            await message.answer(
                "Please send the promotion as text, or tap Main Menu to cancel.",
                reply_markup=submit_menu(),
            )
            return
        await message.answer(
            "Please use the buttons below or /help to see how the bot works.",
            reply_markup=main_menu(),
        )

    return dp


async def main() -> None:
    settings = Settings.from_env()
    storage = Storage(settings.database_path)
    bot = Bot(token=settings.bot_token)
    dp = build_dispatcher(storage, settings)

    logger.info("Starting Starz Promosyon bot")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Starz Promosyon bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
