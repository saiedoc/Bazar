from ClientController import client_controller


class StockmarketDatabinder():

    def get_user_data(user_id):
        """!
        a function that calls the gets the user id from the client controller to the interface
        """
        return client_controller.get_user(user_id)

    def get_all_items(items_dict):
        """!
        a function that calls the gets all items data from the client controller to the interface
        and returns it as dictionary in order to show this data on the interface.
        """
        items = client_controller.get_items()
        for item in items:
            if items_dict.get(item['name']) == None:
                items_dict[item['name']] = []
            items_dict[item['name']].append(item['price'])
        return items_dict

    def get_user_items(items_dict, user_id):
        """!
        a function that calls the gets items data that belongs to a user from the client controller to the interface
        and returns it as dictionary in order to show this data on the interface.
        """
        items = client_controller.get_user_items(user_id)
        for item in items:
            items_dict[item['name']] = item['amount']

        return items_dict

    def update_prices():
        """!
        a function that sends an update prices request in order to update them in the Database in the server side.
        """
        client_controller.update_prices()
