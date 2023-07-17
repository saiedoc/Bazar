import requests
import json


class client_controller:
    base_url = "http://localhost:8000"

    def sign_up(username, password):
        """!
            sign_up API Controller sends a post request to create a new user with the given username and password

            @param username The username
            @param password The password

            @return The id of the new user
        """
        url = f"{client_controller.base_url}/sign-up"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        json_data = json.loads(response.text)
        user_id = json.loads(json_data)
        if user_id == "":
            return None
        else:
            return user_id

    def login(username, password):
        """!
            login API Controller sends a post request to authenticate the user

            @param username The username
            @param password The password

            @return The id of the new user
        """
        url = f"{client_controller.base_url}/login"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, json=data)
        json_data = json.loads(response.text)
        user_id = json.loads(json_data)
        if user_id == "":
            return None
        else:
            return user_id

    def logout(username, password):
        """!
            logout API Controller sends a post request to log out of the account

            @param username The username
            @param password The password
        """
        url = f"{client_controller.base_url}/logout"
        data = {
            "username": username,
            "password": password
        }
        requests.post(url, json=data)

    def sell(amount, item_name, user_id):
        """!
            sell API Controller sends a post request to sell a given amount of items from a user's inventory

            @param amount The amount of the item to be sold
            @param item_name The name of the item
            @param user_id The id of the user
        """
        url = f"{client_controller.base_url}/sell"
        data = {
            "amount": amount,
            "item_name": item_name,
            "user_id": user_id
        }
        requests.post(url, json=data)

    def buy(amount, item_name, user_id):
        """!
            buy API Controller sends a post request to buy a given amount of items

            @param amount The amount of the item to be bought
            @param item_name The name of the item
            @param user_id The id of the user
        """
        url = f"{client_controller.base_url}/buy"
        data = {
            "amount": amount,
            "item_name": item_name,
            "user_id": user_id
        }
        requests.post(url, json=data)

    def get_user_items(user_id):
        """!
            get_user_items API Controller sends a post request to get the items of the user

            @param item_name The name of the item
            @param user_id The id of the user

            @return The list of the requested items
        """
        url = f"{client_controller.base_url}/get-user-items"
        data = {
            "user_id": user_id
        }
        response = requests.post(url, json=data)
        json_data = json.loads(response.text)
        item_list = json.loads(json_data)
        return item_list

    def get_user(user_id):
        """!
            get_user_items API Controller sends a post request to get the user data

            @param user_id The id of the user

            @return The data of the requested user
        """
        url = f"{client_controller.base_url}/get-user"
        data = {
            "user_id": user_id
        }
        response = requests.post(url, json=data)
        json_data = json.loads(response.text)
        item_list = json.loads(json_data)
        return item_list

    def get_items():
        """!
            get_items API Controller sends a get request to get the list of available items

            @return The list of the available items
        """
        url = f"{client_controller.base_url}/get-items"
        response = requests.get(url)
        json_data = json.loads(response.text)
        item_list = json.loads(json_data)
        return item_list

    def pay_in(user_id, amount):
        """!
            pay_in API Controller sends a post request to pay in the given amount to the user's account

            @param user_id The id of the user
            @param amount The amount of money to be paid in
        """
        url = f"{client_controller.base_url}/pay-in"
        data = {
            "user_id": user_id,
            "amount": amount
        }
        requests.post(url, json=data)

    def pay_out(user_id, amount):
        """!
            pay_out API Controller sends a post request to pay out the given amount from the user's account

            @param user_id The id of the user
            @param amount The amount of money to be paid out
        """
        url = f"{client_controller.base_url}/pay-out"
        data = {
            "user_id": user_id,
            "amount": amount
        }
        requests.post(url, json=data)

    def update_prices():
        """!
            update_prices API Controller sends a post request to update the price of the given item
        """
        url = f"{client_controller.base_url}/update-prices"
        requests.post(url)
