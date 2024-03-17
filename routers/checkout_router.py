# Імпортуємо необхідні інструменти
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType

import json
from data import BUTTONS, MESSAGES, TOKENS
from Classes import Cart, Database
from markups import checkout_markups

# Створюємо екземпляри класів роутера та БД
checkout_router = Router(name=__name__)
database = Database()

# При натискані кнопки офрмлення замовлення з меню відбувається наступна функція
@checkout_router.message(F.text == BUTTONS["CHECKOUT"])
# Функція виводу інформаційного повідомлення про замовлення
async def checkout_start_message(message: Message):
    user = Cart.return_user(message.from_user.id) # Повертаємо екземпляр класу користувача
    user_product_list = user.get_user_product_list # Повертаємо кошик користувача

    if len(user_product_list) == 0: # Якщо кошик порожній
        await message.answer(text=MESSAGES["NULL_CART"]) # Інформуємо про цу користувача
        return # Перериваємо функцію
    
    cursor, _ = database.open_connection() # Відкриваємо з'єднання з БД
    user_product_data = [] # Список продуктів для виводу
    
    for product_id in user_product_list: # Пребір усіх елементів списку
        # Додаємо елемент з БД до списку
        user_product_data.append(
            cursor.execute(
                """SELECT id, name, price FROM products_description WHERE id = ?""",
                (product_id,)
            ).fetchone()
        )

    database.close_connection() # Закриваємо з'єднання з БД

    text = "" # Змінна повідомлення
    number = 0 # Змінна для номеру позиції у замовленні

    for product_data in user_product_data: # Пребір усіх елементів списку
        number += 1 
        name = product_data[1]
        price = product_data[2]
        # Створюємо повідомлення
        text += MESSAGES["START_CHECKOUT"].format(
            number=number,
            name=name,
            price=price
        )

    # Відправляємо повідомлення з кнопкою
    await message.answer(text=text,
                         reply_markup=checkout_markups.start_checkout())
    
# При натискані кнопки зворотнього запиту офрмлення замовлення
@checkout_router.callback_query(F.data == "checkout")
# Функція оформлення
async def checkout(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id) # Повертаємо екземпляр класу користувача
    user_product_list = user.get_user_product_list # Повертаємо кошик користувача

    if len(user_product_list) == 0: # Якщо кошик порожній
        await callback.message.answer(text=MESSAGES["NULL_CART"]) # Інформуємо про цу користувача
        return # Перериваємо функцію
    
    cursor, _ = database.open_connection() # Відкриваємо з'єднання з БД
    prices = [] # Створюємо список цін на товари
    
    for product_id in user_product_list: # Перебераємо список
        # Дістаємо інформацію про товар
        data = cursor.execute(
            """SELECT id, name, price FROM products_description WHERE id = ?""",
            (product_id,)
        ).fetchone()
        name = data[1]
        price = data[2]
        # Додаємо ціну
        prices.append(
            LabeledPrice(label=name, amount=price*100)
        )

    database.close_connection() # Закриваємо з'єднання з БД
    # Формуємо та відправляємо повідомлення про оплату
    await callback.message.answer_invoice(
        title=MESSAGES["CHECKOUT"],
        payload=json.dumps({
            "user_id": user.get_user_telegram_id,
            "user_product_list": user.get_user_product_list,
        }),
        description="description",
        provider_token=TOKENS["PAY"],
        currency='UAH',
        prices=prices,
        protect_content=True,
    )

# Перевірка перед оплатою
@checkout_router.pre_checkout_query()
async def pre_checkout(pre_check: PreCheckoutQuery):
    await pre_check.answer(True) # Перевірка успішна

# Дії при успішній оплаті
@checkout_router.message(~F.content_type(ContentType.SUCCESSFUL_PAYMENT))
async def succsess(message: Message):
    payload = json.loads(message.successful_payment.invoice_payload) # Дістаємо діні передані при оплаті
    user_id = payload["user_id"] # З тих даних беремо ID
    product_ids = payload["user_product_list"] # З тих даних беремо ID куплених товарів

    cursor, connection = database.open_connection() # Відкриваємо з'єднання з БД

    for product_id in product_ids: # Проходимо по списку товарів
        # Додаємо замовлення до БД
        cursor.execute(
            """INSERT INTO user_orders(user_id, product_id) VALUES(?, ?)""",
            (user_id, product_id)
        )

    connection.commit() # Підверджуємо дію

    database.close_connection() # Закриваємо з'єднання з БД

    Cart.return_user(user_id=user_id).clear_cart() # Очищаємо корзину еористувача

    await message.answer(text=MESSAGES["PAY_SUCCSESS"]) # Відправляємо повідомлення про успішну оплату
