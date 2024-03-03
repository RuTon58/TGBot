from Classes import User

class Cart:

    __users_list = {}

    @staticmethod
    def add_user_to_cart(user: User) -> None:
        if Cart.__users_list.get(user.get_user_telegram_id) is None:
            Cart.__users_list.update({user.get_user_telegram_id: user})

        
    @staticmethod
    def delete_user_from_cart(user: User) -> None:
        if Cart.__users_list.get(user.get_user_telegram_id) is not None:
            Cart.__users_list.pop(user.get_user_telegram_id)


    @staticmethod
    def __get_user(user_id: int) -> User | None:
        return Cart.__users_list.get(user_id)
    

    @staticmethod
    def return_user(user_id: int) -> User:
        if Cart.__get_user(user_id=user_id) is None:
            Cart.add_user_to_cart(user=User(user_id))
        
        return Cart.__get_user(user_id=user_id)
    

    @staticmethod
    def get_user_list() -> dict:
        return Cart.__users_list
    