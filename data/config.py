TOKENS = {
    "BOT": "5137718377:AAGpyGkP2riOKt_IAgYAITMOEYaQptt8nG4",
    "PAY": "1661751239:TEST:T08k-8bn0-ZW87-odSI",
}

MESSAGES = {
    "START": 'Привіт {name}!\nЦе бот для продажу віртуальних товарів.\nНажміть "Товари 📋" для перегляду наших продуктів',
    "PRODUCT": "{name}\n{discription}\n{price} ₴",
    "NULL_CART": "Кошик порожній",
    "SHOW_CART": "Кошик:",
    "START_CHECKOUT": "{number}. {name} - {price} ₴\n",
    "PAY_SUCCSESS": "Оплата успішна",
    "CHECKOUT": "Оформлення замовлення",
    "ORDER": "Ваші купілені товари",
    "NONE_ORDER": "У Вас немає куплених товарів",
}

BUTTONS = {
    "PRODUCT": "Товари 📋",
    "CART": "Кошик 🧺",
    "CHECKOUT": "Оформити замовлення 💵",
    "ADD_TO_CART": "Додати до кошика ➕",
    "DELETE_FROM_CART": "Видалити з кошика ➖",
    "CART_ITEM_TITLE": "{name} - {price} ₴",
    "CART_CLEAR": "Очистити кошик 🗑️",
    "ORDER_PRODUCT": "Куплено ✔️",
    "ORDERS": "Куплені товари 🚀",
    "ORDERS_ITEM": "{count}. {name}",
}

BUTTONS_DATA = {
    "ADD_TO_CART": "cart_add_{product_id}",
    "DELETE_FROM_CART": "cart_delete_{product_id}",
    "CART_ITEM_TITLE": "cart_item_title_{product_id}",
    "CART_ITEM_TITLE_DELETE": "cart_item_title_delete_{product_id}",
    "CART_CLEAR": "cart_clear",
    "ORDER_PRODUCT": "order_true",
    "CHECKOUT": "checkout",
    "ORDERS_ITEM": "order_item_{product_id}",
}