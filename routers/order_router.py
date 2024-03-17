# Імпортуємо необхідні інструменти
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from data import MESSAGES, BUTTONS, BUTTONS_DATA
from Classes import Cart, Database
from markups import order_markup

# Створюємо екземпляри класів роутера та БД
order_router = Router(name=__name__)
database = Database()

# Виводимо список товарів при натискані на кнопку
@order_router.message(F.text == BUTTONS["ORDERS"])
async def order_show(message: Message):
    user = Cart.return_user(message.from_user.id) # Повертаємо екзепляр класу користувача
    
    if user.refresh_order_list(database=database) is False: # Якщо при оновлені списку куплених товарів не знайдено
        await message.answer(MESSAGES["NONE_ORDER"]) # Повідомлення що користувач не куписв жодного товару
        return # Перериваємо функцію
    
    cursor, _ = database.open_connection() # Відкриваємо з'єднання з БД
    # Знаходимо ID продуктів
    products_ids = [
        cursor.execute(
            """SELECT product_id FROM products_keys WHERE product_description_id = ?""",
            (product_id,)
        ).fetchone() for product_id in user.get_user_ordrer_list
    ]
    # Створюємо список з інормацією
    products_data = [
        cursor.execute(
            """SELECT id, name FROM products WHERE id = ?""",
            (product_id[0],)
        ).fetchone() for product_id in products_ids
    ]

    database.close_connection()
    # Відправляємо список
    await message.answer(text=MESSAGES["ORDER"],
                         reply_markup=order_markup.show_order(products_data))

# При натискані на товар
@order_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["ORDERS_ITEM"].format(product_id="id").split("_")[0:-1])))
# Функція відправки товару
async def get_order_content(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1]) # Дізнаємось ID товару

    cursor, _ = database.open_connection() # Відкриваємо з'єднання з БД
    # Дізнаємось шлях до файлу
    product_path = cursor.execute(
        """SELECT content_path FROM products WHERE id = ?""",
        (product_id,)
    ).fetchone()[0]

    database.close_connection() # Закриваємо зʼєднання з БД
    # Відпраляємо файл користувачу
    await callback.message.answer_document(
        document=FSInputFile(
            path=product_path
        )
    )
