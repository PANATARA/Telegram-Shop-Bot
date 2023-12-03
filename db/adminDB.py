import sqlite3


class AdminShopDB:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def delete_id(self, id):
        with self.connection:
            self.cursor.execute("UPDATE shop SET SHOW = 0 WHERE ID = ?", (id,))

    def disable_all_categories(self, namecat):
        with self.connection:
            self.cursor.execute("UPDATE shop SET SHOW = 0 WHERE CATEGORIES = ?", (namecat,))

    def restore_id(self, id):
        with self.connection:
            self.cursor.execute("UPDATE shop SET SHOW = 1 WHERE ID = ?", (id,))
            
    def add_new_product(self, categories, collection, name,photo, description, color, price):
        with self.connection:
            self.cursor.execute("INSERT INTO shop (CATEGORIES, COLLECTION, NAME, PHOTO, DESCRIPTION, COLOR, PRICE) VALUES (?,?,?,?,?,?,?)", 
                                (categories, collection, name,photo, description, color, price,))  

    def close(self):
        self.connection.close()


