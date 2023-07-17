from database_manager import DatabaseManager
import sqlite3


class stock_service:

    items = ['Diamond', 'Gold', 'Iron', 'Lapis Lazuli',
             'Netherite', 'Redstone', 'Amethyst']

    def __init__(self):
        """!
            The constructor, initializes an instance of DatabaseManager
        """
        self.__db_manager = DatabaseManager(
            "../database/stockmarket_database.db")

        for item in self.items:
            if item == "Amethyst":
                start_value = 5
            elif item == "Diamond":
                start_value = 20
            elif item == "Gold":
                start_value = 10
            elif item == "Iron":
                start_value = 7
            elif item == "Lapis Lazuli":
                start_value = 3
            elif item == "Netherite":
                start_value = 30
            elif item == "Redstone":
                start_value = 6
            self.__db_manager.set_price_stats(item, start_value)

    def get_user_items_list(self, user_id):
        """!
            Returns items of the given type of the user

            @param item_name The name of the item type
            @param user_id The id of the user

            @return The list of the items
        """
        items_list = self.__db_manager.get_user_items(user_id)
        return items_list

    def get_items_list(self):
        """!
            Function to return all items

            @return The list of items
        """
        items_list = self.__db_manager.get_items()
        return items_list

    def buy_items(self, amount, item_name, user_id):
        """!
            Buys the given amount of an item for the given user

            @param amount The amount to be bought
            @param item_name The name of the item
            @param user_id The user
        """

        conn = sqlite3.connect('../database/stockmarket_database.db')
        cursor = conn.cursor()

        getAmountQuery = f"SELECT amount FROM user_items WHERE item_name = ? AND user_id = ?;"
        cursor.execute(getAmountQuery, (item_name, user_id))
        currentAmount = cursor.fetchone()

        query = ""
        if currentAmount is not None and currentAmount[0] > 0:
            query = f"UPDATE user_items SET amount = amount + ? WHERE item_name = ? AND user_id = ?;"
            cursor.execute(query, (amount, item_name, user_id))
        else:
            query = f"INSERT INTO user_items (item_name, amount, user_id) VALUES (?, ?, ?);"
            cursor.execute(query, (item_name, amount, user_id))

        updateBalanceQuery = f"UPDATE user SET balance = balance - ({amount} * (SELECT price FROM items WHERE item_name = ?)) WHERE user_id = ?;"
        cursor.execute(updateBalanceQuery, (item_name, user_id))

        conn.commit()
        conn.close()

    def sell_items(self, amount, item_name, user_id):
        """!
            Sells the given amount of an item from the given user's inventory

            @param amount The amount to be sold
            @param item_name The name of the item
            @param user_id The user
        """
        self.__db_manager.sell(amount, item_name, user_id)

    def sign_up(self, username, password):
        """!
            Signs up the new user

            @param username The chosen username
            @param password The chosen password
        """
        self.__db_manager.add_account(username, password)

    def login(self, username, password):
        """!
            Attempts to log in the user with the given username and password combination

            @param username The username
            @param password The password

            @return The result (success/fail)
        """
        result = self.__db_manager.authenticate_account(username, password)
        return result

    def delete_account(self, username, password):
        """!
            Removes the account from the database

            @param username The username
            @param password The password
        """
        self.__db_manager.remove_account(username, password)

    def in_pay(self, user_id, amount):
        """!
            Pays in the given amount of money to the account of the user

            @param user_id The id of the user
            @param amount The amount of money to be paid in

            @return The amount of money paid in
        """
        self.__db_manager.pay_in(user_id, amount)
        return amount

    def out_pay(self, user_id, amount):
        """!
            Pays out the given amount of money from the account of the user

            @param user_id The id of the user
            @param amount The amount of money to be paid out

            @return The amount of money paid out
        """
        self.__db_manager.pay_out(user_id, amount)
        return amount

    def get_user_id(self, username):
        """!
            Returns the id of the given user

            @param username The username

            @return The id to the given username
        """
        return self.__db_manager.get_userid(username)

    def get_user(self, user_id):
        """!
            Returns user data for a given id

            @param user_id the user_id

            @return The user_data to the given user_id
        """

        conn = sqlite3.connect('../database/stockmarket_database.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username, balance FROM user WHERE user_id = '" + user_id + "';")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        user = {
            "username": results[0][0],
            "balance": results[0][1]
        }
        return user

    def update_prices(self):
        """!
            Updates the price of the given item
        """
        for item in self.items:
            self.__db_manager.update_price(item)
