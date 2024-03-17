from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data import BUTTONS, BUTTONS_DATA

# Функція для створення списку куплених продуктів
def show_order(order_list: list[tuple]) -> InlineKeyboardMarkup:
    inline_list = []
    number = 0

    for product in order_list:
        number += 1
        product_id = product[0]
        product_name = product[1]

        inline_list.append([
            InlineKeyboardButton(
                text=BUTTONS["ORDERS_ITEM"].format(
                    count=number,
                    name=product_name
                ),
                callback_data=BUTTONS_DATA["ORDERS_ITEM"].format(
                    product_id=product_id
                )
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=inline_list)
