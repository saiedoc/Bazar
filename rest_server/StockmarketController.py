from fastapi import FastAPI
import json
import logging
from StockmarketService import stock_service


def ItemtoDict(item):
    return {
        "name": item.name,
        "price": item.price
    }


def UserItemtoDict(item):
    return {
        "name": item.name,
        "amount": item.amount
    }


def UsertoDict(user):
    return {
        "username": user.username,
        "balance": user.balance
    }


class market_controller:

    def __init__(self):
        """!
            The constructor, initializes the FastAPI and an instance of stock_service(), configures the logging
            and creates a logger
        """
        self.app = FastAPI()
        logging.basicConfig(level=logging.INFO)
        self.__stock_service = stock_service()
        self.logger = logging.getLogger()

    def add_account(self, username, password):
        """!
            sign_up API controller function receives a post request with the username and password chosen by the
            new user and calls the add_account function in stock_service

            @param username The username chosen by the new user
            @param password The password chosen by the new user

            @return The username
        """
        self.__stock_service.sign_up(username, password)
        self.logger.info(f"Sign up user request received")
        user_id = self.__stock_service.get_user_id(username)
        json_data = json.dumps(user_id)
        return json_data

    def authenticate_account(self, username, password):
        """!
            login API controller function receives a post request with the username and password
            and calls the authenticate_account function in stock_service

            @param username The username
            @param password The password that belongs to the given user

            @return The id of the user
        """
        result = self.__stock_service.login(username, password)
        self.logger.info(f"Login user request received")
        if result == 1:
            user_id = self.__stock_service.get_user_id(username)
        else:
            user_id = ""
        json_data = json.dumps(user_id)
        return json_data

    def remove_acc(self, username, password):
        """!
            remove_acc API controller function receives a post request with the id of the user and their password to
            confirm they want to delete their account

            @param user_id The id of the user to be deleted from the database
            @param password The password of the user
        """
        self.__stock_service.delete_account(username, password)
        self.logger.info(f"Remove account request received")

    def pay_in(self, user_id, amount):
        """!
            pay_in API controller function receives a post request with the id of the user and the amount of money
            they want to pay in

            @param user_id The id of the user
            @param amount The amount of money the player wants to pay in

            @return The amount of money the user paid in
        """
        self.__stock_service.in_pay(user_id, amount)
        self.logger.info(f"Pay in request received")
        json_data = json.dumps(amount)
        return json_data

    def pay_out(self, user_id, amount):
        """!
            pay_out API controller function receives a post request with the id of the user and the amount of money
            they want to pay out

            @param user_id The id of the user
            @param amount The amount of money the player wants to pay out

            @return The amount of money the user paid out
        """
        self.__stock_service.out_pay(user_id, amount)
        self.logger.info(f"Pay out request received")
        json_data = json.dumps(amount)
        return json_data

    def sell(self, amount, item_name, user_id):
        """!
            sell API controller function receives a post request with the amount and name of the item they want to sell
            and the id of the user

            @param amount The amount of items the user wants to sell
            @param item_name The name of the item that the user wants to sell
            @param user_id The id of the user
        """
        self.__stock_service.sell_items(amount, item_name, user_id)
        self.logger.info(f"Sell item request received")

    def buy(self, amount, item_name, user_id):
        """!
            buy API controller function receives a post request with the amount and name of the item they want to buy
            and the id of the user

            @param amount The amount of items the user wants to buy
            @param item_name The name of the item that the user wants to buy
            @param user_id The id of the user
        """
        self.__stock_service.buy_items(amount, item_name, user_id)
        self.logger.info(f"Buy item request received")

    def get_items(self):
        """!
            get_items API controller function receives a get request and returns the list of all available items

            @return A list of all items available and their prices
        """
        items_list = self.__stock_service.get_items_list()
        items_dict_list = [ItemtoDict(item) for item in items_list]
        self.logger.info(f"Get items list request received")
        json_data = json.dumps(items_dict_list)
        return json_data

    def get_user_items(self, user_id):
        """!
            get_user_items API controller function receives a post request and returns the list of all items of the
            given user

            @param item_name The name of the item we want to know how many of it the given user has
            @param user_id The user whose items we want to see

            @return The item and its amount that the user has
        """
        user_items = self.__stock_service.get_user_items_list(user_id)
        items_dict_list = [UserItemtoDict(item) for item in user_items]
        self.logger.info(f"Get user items list request received")
        json_data = json.dumps(items_dict_list)
        return json_data

    def get_user(self, user_id):
        """!
            get_user API controller function receives a post request and returns user data

            @param user_id the user we are requesting their data.

            @return The item and its amount that the user has
        """
        print("recieved user_id : " + user_id)
        user = self.__stock_service.get_user(user_id)
        self.logger.info(f"Get user data request received")
        print(str(user))
        json_data = json.dumps(user)
        return json_data

    def update_price(self):
        """!
            update_price API controller function receives a post request and returns the new price of the given item

            @param item_name The name of the item
        """
        self.__stock_service.update_prices()
        self.logger.info(f"Update price request received")
