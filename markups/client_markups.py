from data import BUTTONS, BUTTONS_DATA

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def start_markup() -> ReplyKeyboardMarkup:
    products_button = KeyboardButton(text=BUTTONS["PRODUCT"])
    cart_button = KeyboardButton(text=BUTTONS["CART"])
    checkout_button = KeyboardButton(text=BUTTONS["CHECKOUT"])
    orders_button = KeyboardButton(text=BUTTONS["ORDERS"])

    return ReplyKeyboardMarkup(keyboard=[[products_button, cart_button, orders_button], [checkout_button]])


def product_markup(product_id: int, product_in_cart: bool = True, product_in_order: bool = False) -> InlineKeyboardMarkup:
    if product_in_order:
        product_add_to_cart_button = InlineKeyboardButton(text=BUTTONS["ORDER_PRODUCT"],
                                                          callback_data=BUTTONS_DATA["ORDER_PRODUCT"])
        return InlineKeyboardMarkup(inline_keyboard=[[product_add_to_cart_button]])
    
    if product_in_cart is False:
        product_add_to_cart_button = InlineKeyboardButton(text=BUTTONS["ADD_TO_CART"],
                                                          callback_data=BUTTONS_DATA["ADD_TO_CART"].format(
                                                              product_id=product_id
                                                          ))
    else:
        product_add_to_cart_button = InlineKeyboardButton(text=BUTTONS["DELETE_FROM_CART"],
                                                          callback_data=BUTTONS_DATA["DELETE_FROM_CART"].format(
                                                              product_id=product_id
                                                          ))
        
    return InlineKeyboardMarkup(inline_keyboard=[[product_add_to_cart_button]])
