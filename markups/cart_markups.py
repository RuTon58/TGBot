from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import BUTTONS, BUTTONS_DATA


def add_to_cart(product_id: int, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    markup.inline_keyboard[0][0] = InlineKeyboardButton(text=BUTTONS["DELETE_FROM_CART"],
                                                        callback_data=BUTTONS_DATA["DELETE_FROM_CART"].format(
                                                            product_id=product_id
                                                        ))
    
    return markup


def delete_from_cart(product_id: int, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    markup.inline_keyboard[0][0] = InlineKeyboardButton(text=BUTTONS["ADD_TO_CART"],
                                                        callback_data=BUTTONS_DATA["ADD_TO_CART"].format(
                                                            product_id=product_id
                                                        ))
    
    return markup


def show_cart(product_data: list[tuple]) -> InlineKeyboardMarkup:
    inline_list = []

    for product in product_data:
        product_id = product[0]
        product_name = product[1]
        product_price = product[2]

        top_container = [
            InlineKeyboardButton(text=BUTTONS["CART_ITEM_TITLE"].format(name=product_name, 
                                                                        price=product_price),
                                callback_data=BUTTONS_DATA["CART_ITEM_TITLE"].format(product_id=product_id))
        ]

        bottom_container = [
            InlineKeyboardButton(text=BUTTONS["DELETE_FROM_CART"],
                                 callback_data=BUTTONS_DATA["CART_ITEM_TITLE_DELETE"].format(
                                     product_id=product_id
                                 ))
        ]

        inline_list.append(top_container)
        inline_list.append(bottom_container)

    inline_list.append([
        InlineKeyboardButton(text=BUTTONS["CART_CLEAR"],
                             callback_data=BUTTONS_DATA["CART_CLEAR"])
    ])

    return InlineKeyboardMarkup(inline_keyboard=inline_list)


def delete_from_show_cart(product_id: int, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    inline_list = markup.inline_keyboard

    for inline_button in inline_list[0:-1]:
        if int(inline_button[0].callback_data.split("_")[-1]) == product_id:
            inline_list.remove(inline_button)

    return InlineKeyboardMarkup(inline_keyboard=inline_list)

