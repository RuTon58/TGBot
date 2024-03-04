from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile

from data import MESSAGES, BUTTONS, BUTTONS_DATA
from Classes import Cart, Database
from markups import order_markup


order_router = Router(name=__name__)
database = Database()


@order_router.message(F.text == BUTTONS["ORDERS"])
async def order_show(message: Message):
    user = Cart.return_user(message.from_user.id)
    
    if user.refresh_order_list(database=database) is False:
        await message.answer(MESSAGES["NONE_ORDER"])
        return
    
    cursor, _ = database.open_connection()

    products_ids = [
        cursor.execute(
            """SELECT product_id FROM products_keys WHERE product_description_id = ?""",
            (product_id,)
        ).fetchone() for product_id in user.get_user_ordrer_list
    ]

    products_data = [
        cursor.execute(
            """SELECT id, name FROM products WHERE id = ?""",
            (product_id[0],)
        ).fetchone() for product_id in products_ids
    ]

    database.close_connection()

    await message.answer(text=MESSAGES["ORDER"],
                         reply_markup=order_markup.show_order(products_data))

    
@order_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["ORDERS_ITEM"].format(product_id="id").split("_")[0:-1])))
async def get_order_content(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1])

    cursor, _ = database.open_connection()

    product_path = cursor.execute(
        """SELECT content_path FROM products WHERE id = ?""",
        (product_id,)
    ).fetchone()[0]

    database.close_connection()

    await callback.message.answer_document(
        document=FSInputFile(
            path=product_path
        )
    )
