import sqlite3

class ClientShopDB:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


    def get_all_categories(self):

        with self.connection:
            self.cursor.execute("SELECT DISTINCT CATEGORIES FROM shop").fetchall()
            return self.cursor.execute("SELECT DISTINCT CATEGORIES FROM shop").fetchall()
            

    def get_card(self, cat = None, productID = None ):
        with self.connection:

            if cat is not None:
                text = self.cursor.execute(r"SELECT ID, NAME, DESCRIPTION, PRICE FROM shop WHERE CATEGORIES = ? AND SHOW = 1", (cat,)).fetchall()
                photo = self.cursor.execute("SELECT PHOTO FROM shop WHERE CATEGORIES = ? AND SHOW = 1", (cat,)).fetchall()

            if productID is not None:
                text = self.cursor.execute("SELECT ID, NAME, DESCRIPTION, PRICE FROM shop WHERE id = ? AND SHOW = 1", (productID,)).fetchall()
                photo = self.cursor.execute("SELECT PHOTO FROM shop WHERE id = ? AND SHOW = 1", (productID,)).fetchall()

            new_list = []
            for item in text:
                sub_list = []
                for sub_item in item:
                    sub_list.append([r"{}".format(sub_item)])
                new_list.append(sub_list)

            return [new_list, photo]


    def add_product_to_wish_list(self, id, userID, parametr):

        if parametr == "Bag":
            parametr = "UserBag"
            answer = ["Товар добавлен в корзину", "Товар уже у вас в корзине"]
        else:
            parametr = "UserFavorites"
            answer = ["Товар добавлен в избранное!", "Товар уже в избранном"]

        with self.connection:
            self.cursor.execute(f"SELECT * FROM {parametr} WHERE UserID = ? AND ProductId = ?", (userID, id))
            existing_record = self.cursor.fetchone()
            if not existing_record:
                self.cursor.execute(f"INSERT INTO {parametr} (`UserID`,`ProductId` ) VALUES (?, ?)", (userID, id,))
                return answer[0]
            else:
                return answer[1]


    def update_quantity(self, id, userid, operation= None):
        with self.connection:
            if operation != None:
                self.cursor.execute(f"UPDATE UserBag SET quantity = quantity + {int(operation)} WHERE UserId = ? AND ProductID = ? ", (userid, id))
            result = self.cursor.execute(f"SELECT quantity FROM UserBag  WHERE UserId = ? AND ProductID = ? ", (userid, id)).fetchone()
        return result[0]
    

    def get_my_wish_list(self, userID, parametr):

        if parametr == "Bag":
            parametr = "UserBag"
        else:
            parametr = "UserFavorites"

        with self.connection:
            result = self.cursor.execute(f"SELECT ProductId FROM {parametr} WHERE UserId = ?", (userID,)).fetchall()
            result = [item[0] for item in result]
            return result


    def delete_product_from_wish_list(self, id, userID, row):

        wishList = self.get_my_wish_list(userID, row)

        if row == "Bag":
            row = "UserBag"
            answer = "корзины"
        else:
            row = "UserFavorites"
            answer = "избранных"

        if id in wishList:
            with self.connection:
                self.cursor.execute(f"DELETE FROM {row} WHERE ProductId = {id} AND UserId = {userID}")
        return answer


    def get_price(self, userID = None,):
        with self.connection:

            bag = self.cursor.execute("SELECT Productid, quantity FROM UserBag WHERE UserID = ?", (userID,)).fetchall()
            product_quantities = {id_: quantity for id_, quantity in bag}
            total_prices = {}

            for product_id, quantity in product_quantities.items():
                
                price = self.cursor.execute("SELECT price FROM shop WHERE id = ?", (product_id,)).fetchone()[0]

                total_price = int(price) * quantity

                total_prices[product_id] = total_price

            total_sum = sum(total_prices.values())
            return total_sum


    def close(self):
        self.connection.close()
