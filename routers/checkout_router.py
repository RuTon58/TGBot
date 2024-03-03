from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, ContentType

import json
from data import BUTTONS, MESSAGES, TOKENS
from Classes import Cart, Database
from markups import checkout_markups


checkout_router = Router(name=__name__)
database = Database()


@checkout_router.message(F.text == BUTTONS["CHECKOUT"])
async def checkout_start_message(message: Message):
    user = Cart.return_user(message.from_user.id)
    user_product_list = user.get_user_product_list

    if len(user_product_list) == 0:
        await message.answer(text=MESSAGES["NULL_CART"])
        return
    
    cursor, _ = database.open_connection()
    user_product_data = []
    
    for product_id in user_product_list:
        user_product_data.append(
            cursor.execute(
                """SELECT id, name, price FROM products_description WHERE id = ?""",
                (product_id,)
            ).fetchone()
        )

    database.close_connection()

    text = ""
    number = 0

    for product_data in user_product_data:
        number += 1
        name = product_data[1]
        price = product_data[2]

        text += MESSAGES["START_CHECKOUT"].format(
            number=number,
            name=name,
            price=price
        )


    await message.answer(text=text,
                         reply_markup=checkout_markups.start_checkout())
    

@checkout_router.callback_query(F.data == "checkout")
async def checkout(callback: CallbackQuery):
    user = Cart.return_user(callback.from_user.id)
    user_product_list = user.get_user_product_list

    if len(user_product_list) == 0:
        await callback.message.answer(text=MESSAGES["NULL_CART"])
        return
    
    cursor, _ = database.open_connection()
    prices = []
    
    for product_id in user_product_list:
        data = cursor.execute(
            """SELECT id, name, price FROM products_description WHERE id = ?""",
            (product_id,)
        ).fetchone()
        name = data[1]
        price = data[2]
        prices.append(
            LabeledPrice(label=name, amount=price*100)
        )

    database.close_connection()

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


@checkout_router.pre_checkout_query()
async def pre_checkout(pre_check: PreCheckoutQuery):
    await pre_check.answer(True)


@checkout_router.message(~F.content_type(ContentType.SUCCESSFUL_PAYMENT))
async def succsess(message: Message):
    payload = json.loads(message.successful_payment.invoice_payload)
    user_id = payload["user_id"]
    product_ids = payload["user_product_list"]

    cursor, connection = database.open_connection()

    for product_id in product_ids:
        cursor.execute(
            """INSERT INTO user_orders(user_id, product_id) VALUES(?, ?)""",
            (user_id, product_id)
        )

    connection.commit()

    database.close_connection()

    Cart.return_user(user_id=user_id).clear_cart()

    await message.answer(text=MESSAGES["PAY_SUCCSESS"])
