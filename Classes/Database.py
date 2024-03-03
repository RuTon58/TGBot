import sqlite3

class Database:

    __path = ""

    def __init__(self, path: str = None) -> None:
        if path is not None:
            Database.__path = path
        
        self.__conection: sqlite3.Connection = None


    def open_connection(self) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
        self.__conection = sqlite3.connect(Database.__path)
        cursor = self.__conection.cursor()

        return cursor, self.__conection
    

    def close_connection(self) -> None:
        self.__conection.close()
        