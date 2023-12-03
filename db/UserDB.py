import sqlite3

class UserDB:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по user_id"""
        result = self.cursor.execute("SELECT `ID` FROM users WHERE `User_ID` = ?", (user_id,))
        return result.fetchone()[0]

    def get_all_user_id(self):
        result = self.cursor.execute("SELECT user_id FROM users")
        return result.fetchall()

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO users (`User_ID`) VALUES (?)", (user_id,))
        return self.connection.commit()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()