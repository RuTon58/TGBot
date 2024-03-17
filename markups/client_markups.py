# Імпортуємо необхідні інструменти
from data import BUTTONS, BUTTONS_DATA

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


# Функція яка повертає головне меню користувачу
def start_markup() -> ReplyKeyboardMarkup:
    products_button = KeyboardButton(text=BUTTONS["PRODUCT"])
    cart_button = KeyboardButton(text=BUTTONS["CART"])
    checkout_button = KeyboardButton(text=BUTTONS["CHECKOUT"])
    orders_button = KeyboardButton(text=BUTTONS["ORDERS"])

    return ReplyKeyboardMarkup(keyboard=[[products_button, cart_button, orders_button], [checkout_button]])

# Функція яка повертає розмітку вбудованої клавіатури для додавання або видалення товару з кошика
def product_markup(product_id: int, product_in_cart: bool = True, product_in_order: bool = False) -> InlineKeyboardMarkup:
    # Якщо товар є в куплених то виводимо кнопку "Куплено"
    if product_in_order:
        product_add_to_cart_button = InlineKeyboardButton(text=BUTTONS["ORDER_PRODUCT"],
                                                          callback_data=BUTTONS_DATA["ORDER_PRODUCT"])
        return InlineKeyboardMarkup(inline_keyboard=[[product_add_to_cart_button]])
    # Якщо товару немає в кошику то виводимо кнопку "Додати"
    if product_in_cart is False:
        product_add_to_cart_button = InlineKeyboardButton(text=BUTTONS["ADD_TO_CART"],
                                                          callback_data=BUTTONS_DATA["ADD_TO_CART"].format(
                                                              product_id=product_id
                                                          ))
    # Якщо товар є в кошику то виводимо кнопку "Видалити"
    else:
        product_add_to_cart_button = InlineKeyboardButton(text=BUTTONS["DELETE_FROM_CART"],
                                                          callback_data=BUTTONS_DATA["DELETE_FROM_CART"].format(
                                                              product_id=product_id
                                                          ))
        
    return InlineKeyboardMarkup(inline_keyboard=[[product_add_to_cart_button]])
