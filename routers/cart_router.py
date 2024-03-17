# Імпортуємо необхідні інструменти
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from Classes import Cart, Database
from data import BUTTONS_DATA, BUTTONS, MESSAGES
from markups import cart_markups

# Створюємо екземпляри класів роутер і БД
cart_router = Router(name=__name__)
database = Database()

# Слухаємо зворотній запит від встроєноЇ клавіатури на додавання товару до кошика
@cart_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["ADD_TO_CART"].format(product_id="id").split("_")[0:-1])))
# Функція додавання до кошика
async def add_to_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id) # Повертаємо об'єкт користувача
    markup = callback.message.reply_markup # Беремо клавіатуру з зворотнього запиту
    product_id = int(callback.data.split("_")[-1]) # Беремо ID товару
    markup = cart_markups.add_to_cart(product_id=product_id, markup=markup) # Змінюємо клавіатуру

    user.add_to_user_cart(product_id=product_id) # Додаємо товар до кошика користувача

    await callback.message.edit_reply_markup(reply_markup=markup) # Змінюємо клавіатуру у повідомлені

# Слухаємо зворотній запит від встроєноЇ клавіатури на видалення товару з кошика
@cart_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["DELETE_FROM_CART"].format(product_id="id").split("_")[0:-1])))
# Функція видалення з кошика
async def delete_from_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id) # Повертаємо об'єкт користувача
    markup = callback.message.reply_markup # Беремо клавіатуру з зворотнього запиту
    product_id = int(callback.data.split("_")[-1]) # Беремо ID товару
    markup = cart_markups.delete_from_cart(product_id=product_id, markup=markup) # Змінюємо клавіатуру

    user.delete_from_user_cart(product_id=product_id) # Видаляємо товар з кошика користувача

    await callback.message.edit_reply_markup(reply_markup=markup) # Змінюємо клавіатуру у повідомлені
    
# При натискані на кнопку корзини буде відкликатися ця функція
@cart_router.message(F.text == BUTTONS["CART"])
# Функція для виводу кошика
async def show_cart(message: Message):
    user = Cart.return_user(message.from_user.id) # Повертаємо об'єкт користувача 
    user_product_list = user.get_user_product_list # Дістаємо з нього список товарів у кошику

    if len(user_product_list) == 0: # Якщо кошик пустий 
        await message.answer(MESSAGES["NULL_CART"]) # Інформуємо про це користувача повідомленням
        return # Перериваємо функцію
    
    cursor, _ = database.open_connection() # Відкриваємо з'єднання з БД

    user_product_data = [] # Створюємо пустий список

    for product_id in user_product_list: # Перебираємо всі елементи списку товарів
        # Додаємо до пустого списку необхідну інформацію про товар з БД
        user_product_data.append(cursor.execute("SELECT id, name, price FROM products_description WHERE id = ?",
                                                (product_id,)).fetchone())

    database.close_connection() # Закриваємо з'єднання з БД
    # Відправляємо користувачу повідомлення про зміст його кошика
    await message.answer(text=MESSAGES["SHOW_CART"],
                         reply_markup=cart_markups.show_cart(user_product_data))
    
# Слухаємо зворотній запит від встроєноЇ клавіатури на видалення товару з відображеного кошика
@cart_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["CART_ITEM_TITLE_DELETE"].format(product_id="id").split("_")[0:-1])))
# Функція для видалення
async def delete_from_show_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id) # Повертаємо об'єкт користувача
    product_id = int(callback.data.split("_")[-1]) # Беремо ID товару
    markup = callback.message.reply_markup # Беремо клавіатуру з зворотнього запиту

    if len(user.get_user_product_list) == 0: # Якщо кошик пустий
        return # Перериваємо функцію
    
    user.delete_from_user_cart(product_id=product_id) # Видаляємо товар з кошика
    # Змінюємо список та повертаємо новий
    await callback.message.edit_reply_markup(
        reply_markup=cart_markups.delete_from_show_cart(product_id=product_id,
                                                        markup=markup)
    )

# Слухаємо зворотній запит від встроєноЇ клавіатури на очищення кошика
@cart_router.callback_query(F.data == BUTTONS_DATA["CART_CLEAR"])
# Функція очищення кошика
async def clear_show_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id) # Повертаємо об'єкт користувача

    if len(user.get_user_product_list) == 0: # Якщо кошик пустий
        return # Перериваємо функцію
    
    user.clear_cart() # Очищаємо кошик користувача

    await callback.message.edit_reply_markup() # Повертаємо пусту клавіатуру
