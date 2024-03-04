from Classes import Database, User, Cart

db = Database("data/sqlite_database.db")

cursor, connection = db.open_connection()

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
# cursor.execute("INSERT INTO products_description(name, discription, image, price) VALUES (?, ?, ?, ?)",
#                ("NAME", "DISCRIPTION", "images/product_1.png", 1000))
# cursor.execute("INSERT INTO products_description(name, discription, image, price) VALUES (?, ?, ?, ?)",
#                ("NAME", None, "images/product_1.png", 1000))
# cursor.execute("INSERT INTO products_description(name, discription, image, price) VALUES (?, ?, ?, ?)",
#                ("NAME", "DISCRIPTION", None, 1000))

# cursor.execute("INSERT INTO products_keys(product_description_id, product_id) VALUES (?, ?)",
#                (1, 1))
# cursor.execute("INSERT INTO products_keys(product_description_id, product_id) VALUES (?, ?)",
#                (2, 1))
# cursor.execute("INSERT INTO products_keys(product_description_id, product_id) VALUES (?, ?)",
#                (3, 1))
# cursor.execute("DELETE FROM products_description")
cursor.execute("DELETE FROM user_orders")
# cursor.execute("DELETE FROM products")
# cursor.execute("DELETE FROM products_keys")

# cursor.execute("INSERT INTO products_description(name, discription, image, price) VALUES (?, ?, ?, ?)",
#                ("Відео", "Тут ви придбаєте відео контент", "images/video.png", 100))
# cursor.execute("INSERT INTO products_description(name, discription, image, price) VALUES (?, ?, ?, ?)",
#                ("Музика", "Тут ви придбаєте музичний контент", "images/music.jpg", 100))
# cursor.execute("INSERT INTO products(name, content_path) VALUES (?, ?)",
#                ("Музика", "content/music.mp3"))
# cursor.execute("INSERT INTO products(name, content_path) VALUES (?, ?)",
#                ("Відео", "content/video.mp4"))
# cursor.execute("INSERT INTO products_keys(product_description_id, product_id) VALUES (?, ?)",
#                (4, 3))
# cursor.execute("INSERT INTO products_keys(product_description_id, product_id) VALUES (?, ?)",
#                (5, 2))
connection.commit()

print(cursor.execute("SELECT * FROM products_description").fetchall())
print(cursor.execute("SELECT * FROM products").fetchall())
print(cursor.execute("SELECT * FROM products_keys").fetchall())

db.close_connection()

print("_".join("call_back_1".split("_")[-1]))