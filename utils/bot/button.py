from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

start_button = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("List saved words", callback_data="list_words")
        ],
    ]
)
def post_button(bot_username:str, word:str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Save ⭐️", callback_data=f"save_{word}"),
                InlineKeyboardButton("Take a quiz", url=f"https://t.me/{bot_username}?start=quiz_{word}")
            ],
            [
                InlineKeyboardButton(f"📘 More about {word}", url=f"https://t.me/{bot_username}?start=word_{word}")
            ]
        ]
    )
