from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from Classes import Cart, Database
from data import BUTTONS_DATA, BUTTONS, MESSAGES
from markups import cart_markups


cart_router = Router(name=__name__)
database = Database()


@cart_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["ADD_TO_CART"].format(product_id="id").split("_")[0:-1])))
async def add_to_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id)
    markup = callback.message.reply_markup
    product_id = int(callback.data.split("_")[-1])
    markup = cart_markups.add_to_cart(product_id=product_id, markup=markup)

    user.add_to_user_cart(product_id=product_id)

    await callback.message.edit_reply_markup(reply_markup=markup)


@cart_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["DELETE_FROM_CART"].format(product_id="id").split("_")[0:-1])))
async def delete_from_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id)
    markup = callback.message.reply_markup
    product_id = int(callback.data.split("_")[-1])
    markup = cart_markups.delete_from_cart(product_id=product_id, markup=markup)

    user.delete_from_user_cart(product_id=product_id)

    await callback.message.edit_reply_markup(reply_markup=markup)
    

@cart_router.message(F.text == BUTTONS["CART"])
async def show_cart(message: Message):
    user = Cart.return_user(message.from_user.id)
    user_product_list = user.get_user_product_list

    if len(user_product_list) == 0:
        await message.answer(MESSAGES["NULL_CART"])
        return
    
    cursor, _ = database.open_connection()

    user_product_data = []

    for product_id in user_product_list:
        user_product_data.append(cursor.execute("SELECT id, name, price FROM products_description WHERE id = ?",
                                                (product_id,)).fetchone())

    database.close_connection()

    await message.answer(text=MESSAGES["SHOW_CART"],
                         reply_markup=cart_markups.show_cart(user_product_data))
    

@cart_router.callback_query(F.data.startswith("_".join(BUTTONS_DATA["CART_ITEM_TITLE_DELETE"].format(product_id="id").split("_")[0:-1])))
async def delete_from_show_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id)
    product_id = int(callback.data.split("_")[-1])
    markup = callback.message.reply_markup

    if len(user.get_user_product_list) == 0:
        return
    
    user.delete_from_user_cart(product_id=product_id)

    await callback.message.edit_reply_markup(
        reply_markup=cart_markups.delete_from_show_cart(product_id=product_id,
                                                        markup=markup)
    )


@cart_router.callback_query(F.data == BUTTONS_DATA["CART_CLEAR"])
async def clear_show_cart(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id)
    markup = callback.message.reply_markup

    if len(user.get_user_product_list) == 0:
        return
    
    user.clear_cart()

    await callback.message.edit_reply_markup()
