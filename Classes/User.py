from Classes import Database

class User:
    
    def __init__(self, telegram_id: int) -> None:
        self.__telegram_id: int = telegram_id
        self.__product_list: list = []
        self.__orders_list: list = []


    def add_to_user_cart(self, product_id: int) -> None:
        if product_id not in self.__product_list:
            self.__product_list.append(product_id)


    def delete_from_user_cart(self, product_id: int) -> None:
        if product_id in self.__product_list:
            self.__product_list.remove(product_id)


    def clear_cart(self) -> None:
        self.__product_list.clear()


    def product_in_cart(self, product_id: int) -> bool:
        return True if product_id in self.__product_list else False


    def refresh_order_list(self, database: Database) -> bool:
        cursor, _ = database.open_connection()

        order_list = cursor.execute(
            """SELECT product_id FROM user_orders WHERE user_id = ?""",
            (self.__telegram_id,)
        ).fetchall()

        database.close_connection

        if len(order_list) == 0:
            return False
        
        self.__orders_list = [int(order[0]) for order in order_list]
        
        return True



    def product_in_order_list(self, product_id: int) -> bool:
        return True if product_id in self.__orders_list else False


    @property
    def get_user_product_list(self) -> list:
        return self.__product_list


    @property
    def get_user_ordrer_list(self) -> list:
        return self.__orders_list


    @property
    def get_user_telegram_id(self) -> int:
        return self.__telegram_id
    