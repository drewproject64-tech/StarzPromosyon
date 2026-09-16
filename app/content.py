from dataclasses import dataclass


@dataclass(frozen=True)
class Item:
    title: str
    body: str


PROMOTIONS = (
    Item(
        "Featured promotions",
        "Browse promotional opportunities published inside Starz Promosyon. "
        "All details are shown here in Telegram; there is no external redirect.",
    ),
    Item(
        "Campaign showcase",
        "A campaign can include its title, purpose, audience and key details. "
        "Use Submit Promotion if you want to send a promotion for consideration.",
    ),
    Item(
        "Promotion guidelines",
        "Keep submitted promotions clear, accurate and relevant. Do not include "
        "passwords, payment credentials or other private information.",
    ),
)

UPDATES = (
    Item(
        "Starz Promosyon",
        "This bot is designed as a Telegram-native promotion information hub. "
        "Its core content and navigation are available directly in the chat.",
    ),
    Item(
        "In-app content",
        "Promotional information and updates are presented as Telegram messages "
        "and buttons, so users can read and navigate without leaving the bot.",
    ),
    Item(
        "Submission flow",
        "The submission form validates the message before saving it. A saved "
        "submission receives a reference number for follow-up.",
    ),
)
