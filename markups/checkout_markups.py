# Імпортуємо необхідні інструменти
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import BUTTONS, BUTTONS_DATA

# Функція для кнопку оформлення замовлення
def start_checkout() -> InlineKeyboardMarkup:
    # Створюємо кнопку
    checkout_button = InlineKeyboardButton(text=BUTTONS["CHECKOUT"],
                                           callback_data=BUTTONS_DATA["CHECKOUT"])
    # Повертаємо кнопку
    return InlineKeyboardMarkup(inline_keyboard=[[checkout_button]])
