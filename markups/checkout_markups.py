from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Classes import User
from data import BUTTONS, BUTTONS_DATA


def start_checkout() -> InlineKeyboardMarkup:
    checkout_button = InlineKeyboardButton(text=BUTTONS["CHECKOUT"],
                                           callback_data=BUTTONS_DATA["CHECKOUT"])
    
    return InlineKeyboardMarkup(inline_keyboard=[[checkout_button]])
