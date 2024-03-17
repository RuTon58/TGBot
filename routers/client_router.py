# Імпортуємо необхідні інструменти
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart

from Classes import Database, Cart
from data import MESSAGES, BUTTONS

from markups import client_markups
from routers.cart_router import cart_router
from routers.checkout_router import checkout_router
from routers.order_router import order_router

# Створюємо роутер
client_router = Router(name=__name__)
# Підключаємо інші роутери до клієнтського
client_router.include_router(cart_router)
client_router.include_router(order_router)
client_router.include_router(checkout_router)
# Створюємо екземпляр БД
database = Database()

# Оголошеємо хендлер який обробляє команду запуску бота
@client_router.message(CommandStart())
# Функція яка відправляє стартове повідомлення
async def start(message: Message):
    await message.answer(text=MESSAGES["START"].format(name=message.from_user.full_name), 
                         reply_markup=client_markups.start_markup())    
    
# Оголошеємо хендлер який спрацьовує при необхідній кнопці
@client_router.message(F.text == BUTTONS["PRODUCT"])
# Функція відправки списку продуктів
async def product(message: Message):
    # Беремо єкземпляр користувача та оновлюємо список куплених товарів
    user = Cart.return_user(message.from_user.id)
    user.refresh_order_list(database=database)
    # Відкриваємо з'єднання з БД 
    cursor, _ = database.open_connection()
    # Дістаємо усе з таблиці опису товарів
    product_list = cursor.execute("SELECT * FROM products_description").fetchall()
    # Закриваємо з'єднання
    database.close_connection()

    # Проходимо по кожному товару
    for product_data in product_list:
        # Записуємо усе у змінні
        product_id = product_data[0]
        product_name = product_data[1]
        # Якщо опис пустий то змінна дорівнює пустій строчці
        product_discription = product_data[2] if product_data[2] is not None else ""
        product_price = product_data[4]
        product_image = product_data[3]
        # Опис для повідомлення
        caption = MESSAGES["PRODUCT"].format(name=product_name,
                                             discription=product_discription,
                                             price=product_price)
        # Змінна для клавіатури, яка буде видаляти або додавати до кошика
        product_markup = client_markups.product_markup(product_id=product_id,
                                                       product_in_cart=user.product_in_cart(product_id=product_id),
                                                       product_in_order=user.product_in_order_list(product_id=product_id))
        # Якщо немає картинки то відправляємо повідомлення
        if product_image is None:
            await message.answer(text=caption, 
                                 reply_markup=product_markup)
            continue
        # Якщо є фото то відправляємо повідомлення
        await message.answer_photo(photo=FSInputFile(path=product_image),
                                   caption=caption,
                                   reply_markup=product_markup)
        



