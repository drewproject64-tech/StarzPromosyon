from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Promotions", callback_data="promotions")],
            [InlineKeyboardButton(text="ℹ️ About", callback_data="about")],
        ]
    )


def promotion_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Example Promotion", callback_data="example_promotion")],
            [InlineKeyboardButton(text="⬅️ Back", callback_data="back_home")],
        ]
    )


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back", callback_data="back_home")]]
    )
