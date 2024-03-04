from Classes import Database


def create_database(database: Database) -> None:
    cursor, connection = database.open_connection()

    cursor.execute("""CREATE TABLE IF NOT EXISTS products_description (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               discription TEXT,
               image TEXT, 
               price INTEGER NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS user_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                content_path TEXT NOT NULL
    )""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS products_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_description_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL
    )""")

    database.close_connection()
