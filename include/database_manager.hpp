#pragma once
#include <sqlite3.h>
#include <iostream>
#include <memory>
#include <vector>
#include <utility>
#include <random>
#include <cmath>
#include "boost/uuid/uuid_generators.hpp"
#include "boost/uuid/uuid.hpp"
#include "boost/uuid/uuid_io.hpp"

/**
 * @brief Represents a user with his amount of an item.
 */
struct User_amount {
    int amount; /**< The amount of the item a user holds*/
};

/**
 * @brief Represents an item with name and price.
 */
struct Item
{
    std::string name; /**< The name of the item. */
    float price;      /**< The price of the item. */
};

/**
 * @brief Represents an item possesed by a user with name, amount and price.
 */
struct Item_user
{
    std::string name; /**< The name of the item. */
    int amount;       /**< The amount of the item possesed by the user. */
    int price;        /**< The price of the item. */
};

/**
 * @brief Represents statistics related to an item.
 */
struct Stats
{
    float tendence;           /**< The tendency value of the item. */
    float standard_deviation; /**< The standard deviation of the item. */
    float current_price;      /**< The current price of the item. */
};

/**
 * @brief Represents a user with name and balance
 */
struct User
{
    std::string username; /**< The username of the user. */
    int balance;          /**< The balance of the user. */
};

/**
 * @brief The DatabaseManager class for managing SQLite database connections and operations.
 */
class DatabaseManager
{
public:
    /**
     * @brief Constructs a new DatabaseManager object and establishes a connection to
     * the specified database.
     * @param dbName The name of the database to connect to (e.g. database.db)
     */
    DatabaseManager(const std::string &dbName);

    /**
     * @brief Connects to the specified database.
     * If a connection is already open, it is closed before establishing a new connection.
     * @param dbName The name of the database to connect to (e.g. database.db)
     */
    void connect(const std::string &dbName);

    /**
     * @brief Status of connection
     * @return True if connected to database, false otherwise.
     */
    bool status();

    /**
     * @brief Checks if a specific table exists
     * @return True if it exists, false otherwise,
     * @note This function assumes a valid database connection.
     */
    bool tableExists(const std::string &tableName);

    /**
     * @brief Closes the database connection.
     * @note This function assumes a valid database connection.
     */
    void closeDatabase();

    /**
     * @brief Executes the specified SQL query on the connected database.
     * @param query The SQL query to execute.
     * @note This function assumes a valid database connection.
     */
    void executeQuery(const std::string &query);

    /**
     * @brief Insert data into the specified table from the connected database.
     * Example:
     * insertTable("myTable", "420, 'Jo Mom'");
     * @param tableName The name of the table
     * @param data The data to insert
     * @note This function assumes a valid database connection.
     */
    void insertTable(const std::string &tableName, const std::string &data);

    /**
     * @brief Prints the specified table
     * @param tableName The name of the table to be printed
     * @note This function assumes a valid database connection.
     */
    void showTable(const std::string &tableName);

    /**
     * @brief Retrieves the items and their amounts for a specific user from the database.
     * @param user_id The ID of the user to retrieve items for.
     * @return A vector of Item objects representing the user's items and amounts.
     * @note This function assumes a valid database connection.
     */
    std::vector<Item_user> get_user_items(const std::string &user_id);

    /**
     * @brief Retrieves all items and their prices from the database.
     * @return A vector of Item objects representing the items and their prices.
     * @note This function assumes a valid database connection.
     */
    std::vector<Item> get_items();

    /**
     * @brief Retrieves the username and users balance
     * @param user_id The user_id of the user
     * @return a vector of ... representing the user's name and balance
     * @note This function assumes a valid database connection
     */
    User get_user(const std::string &user_id);

    /**
     * @brief Retrieves the user_id of the specific username
     * @param username The name of the user
     * @return A string of the user_id
     * @note This function assumes a balid database connection.
     */
    std::string get_userid(const std::string &username);

    /**
     * @brief Buys a specified amount of an item for a user.
     * @param amount The amount of the item to be bought.
     * @param itemName The name of the item to be bought.
     * @param user_id The ID of the user making the purchase.
     * @note This function assumes a valid database connection.
     */
    void buy(int amount, const std::string &itemName, const std::string &user_id);

    /**
     * @brief Sells a specified amount of an item by updating the item's amount in the user_items table
     *        and the user's balance in the user table.
     * @param amount The amount of the item to be sold.
     * @param itemName The name of the item to be sold.
     * @param user_id The ID of the user making the sale.
     * @note This function assumes a valid database connection.
     */
    void sell(int amount, const std::string &itemName, const std::string &user_id);

    /**
     * @brief Adds a new user account with the provided username and password.
     * @param username The username for the new account.
     * @param password The password for the new account.
     * @note If the username already exists, the function prints an error message and returns without creating a new account.
     * @note This function assumes a valid database connection.
     */
    void add_account(std::string username, std::string password);

    /**
     * @brief Authenticates a user account with the provided username and password.
     * @param username The username of the account to authenticate.
     * @param password The password of the account to authenticate.
     * @return True if the account is authenticated, false otherwise.
     * @note This function assumes a valid database connection.
     */
    bool authenticate_account(std::string username, std::string password);

    /**
     * @brief Adds cash to a user's balance.
     * @param user_id The name of the user.
     * @param amount The amount to be added to the user's balance.
     * @note This function assumes a valid database connection.
     */
    void pay_in(std::string user_id, int amount);

    /**
     * @brief Withdraws cash from a user's balance.
     * @param user_id The name of the user.
     * @param amount The amount to be deducted from the user's balance.
     * @note This function assumes a valid database connection.
     */
    void pay_out(std::string user_id, int amount);

    /**
     * @brief Removes a user account from the database.
     * @param username The username of the account to be removed.
     * @param password The password of the account to be removed.
     * @note This function assumes a valid database connection.
     */
    void remove_account(std::string username, std::string password);

    /**
     * @brief Adds a new item into the items table with all attributes equal to 0
     * @note This function assumes a valid database connection.
     */
    void add_new_item(const std::string &itemName);

    /**
     * @brief Sets the values of our Item and generates a course
     * @param item_name The name of the item
     * @note This function does not set the price just the stats for it to be calculated.
     * @note This function assumes a valid database connection.
     */
    void set_price_stats(std::string item_name, int start_value);

    /**
     * @brief Updates the prices in the items table for the specified item
     * @param itemName The name of the item to be updated
     * @note This function assumes a valid database connection.
     */
    void update_price(std::string itemName);

private:
    sqlite3 *db; /*!< The SQLite database connection pointer. */

    /**
     * @brief Callback function used to process rows of the result set and print them.
     * =>it prints tabels
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int print(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Callback function used to safe the user's items and their amount
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int safe_user_items(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Callback function used to safe the items and their price
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int safe_items(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Callback function used to safe the user_id
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int safe_user_id(void *data, int column_count, char **column_values, char **column_name);
    
    /**
     * @brief Callback function used to safe the user_id
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     * @note If the ptr equals nullptr this implies that the user doesnt have this item and else he has 
     */
    static int safe_amount(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Callback function used to safe the user
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int safe_user(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Callback function used to check if something exists
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int exists(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Function which checks if as username already exists
     * @param username The username to check for existens
     * @return bool indicating if the username exists
     * true = exists, false = not existing
     */
    bool username_exists(std::string username);

    /**
     * @brief Callback function used to safe the tendence, current_price and standard_deviation
     *        of an Item
     *
     * @param data A generic pointer to additional data
     * @param column_count The number of columns in the current row of the result set.
     * @param column_values An array of strings representing the values of each column in the current row.
     * @param column_name An array of strings containing the names of each column in the result set.
     *
     * @return An integer indicating the status of the callback function.
     *         Returning 0 indicates success.
     */
    static int safe_stats(void *data, int column_count, char **column_values, char **column_name);

    /**
     * @brief Function which generates one randomWalk value
     *
     * @param tendence The tendency of the market value (how strong should the price rise over the long term)
     * @param standard_deviation The standard deviation (die Streuung) of the market value
     * @param dt The size of the time step
     * @param current_price The current price of an item
     *
     * @return An float representing the new price for an item
     */
    float generateRandomWalk_value(float tendence, float standard_deviation, float dt, int current_price);
};
