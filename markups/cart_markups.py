# Імпортуємо необхідні інструментиє
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import BUTTONS, BUTTONS_DATA

# Функція для зміни клавіатури після додавання до кошика
def add_to_cart(product_id: int, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    # Змінюємо клавіатуру яку передили як аргумент
    markup.inline_keyboard[0][0] = InlineKeyboardButton(text=BUTTONS["DELETE_FROM_CART"],
                                                        callback_data=BUTTONS_DATA["DELETE_FROM_CART"].format(
                                                            product_id=product_id
                                                        ))
    # Вертаємо клавіатуру
    return markup

# Функція для зміни клавіатури після видалення з кошика
def delete_from_cart(product_id: int, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    # Змінюємо клавіатуру яку передили як аргумент
    markup.inline_keyboard[0][0] = InlineKeyboardButton(text=BUTTONS["ADD_TO_CART"],
                                                        callback_data=BUTTONS_DATA["ADD_TO_CART"].format(
                                                            product_id=product_id
                                                        ))
    # Вертаємо клавіатуру
    return markup

# Функція створення вбудованої клавіатури виводу зміста кошика
def show_cart(product_data: list[tuple]) -> InlineKeyboardMarkup:
    inline_list = [] # список куди ми будемо додавати кнопки
    # Перебераємо усі еламенти списку
    for product in product_data:
        product_id = product[0] # Назначаємо ID
        product_name = product[1] # Назначаємо ім'я
        product_price = product[2] # Назначаємо ціну
        # Створюємо верхню частину з ім'ям та ціною товару
        top_container = [
            InlineKeyboardButton(text=BUTTONS["CART_ITEM_TITLE"].format(name=product_name, 
                                                                        price=product_price),
                                callback_data=BUTTONS_DATA["CART_ITEM_TITLE"].format(product_id=product_id))
        ]
        # Створюємо нижню частину з видаленням елементу з кошика
        bottom_container = [
            InlineKeyboardButton(text=BUTTONS["DELETE_FROM_CART"],
                                 callback_data=BUTTONS_DATA["CART_ITEM_TITLE_DELETE"].format(
                                     product_id=product_id
                                 ))
        ]
        # Додаємо кнопки до списку
        inline_list.append(top_container)
        inline_list.append(bottom_container)
    # Додаємо кнопку очищення кошика
    inline_list.append([
        InlineKeyboardButton(text=BUTTONS["CART_CLEAR"],
                             callback_data=BUTTONS_DATA["CART_CLEAR"])
    ])
    # Повертаємо клавіатуру
    return InlineKeyboardMarkup(inline_keyboard=inline_list)

# Функція видалення товару з списку кошика
def delete_from_show_cart(product_id: int, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
    inline_list = markup.inline_keyboard # Дістаємо кнопки з клавіатури

    for inline_button in inline_list[0:-1]: # Перебераємо всі кнопки крім кнопки очищення кошика
        if int(inline_button[0].callback_data.split("_")[-1]) == product_id: # Якщо кнопка має потрібний ID
            inline_list.remove(inline_button) # Визаляємо кнопку

    return InlineKeyboardMarkup(inline_keyboard=inline_list) # Повертаємо клавіатуру

