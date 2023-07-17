#include "../include/database_manager.hpp"

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

DatabaseManager::DatabaseManager(const std::string &dbName) : db(nullptr)
{
    connect(dbName);
}

void DatabaseManager::connect(const std::string &dbName)
{
    // close the existing database connection if it's open
    if (db != nullptr)
    {
        sqlite3_close(db);
        db = nullptr;
    }
    // connect to dbName
    // db will point to the database
    int rc = sqlite3_open(dbName.c_str(), &db);
    // error handling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to open database.");
    }
}

bool DatabaseManager::status()
{
    if (db == nullptr)
    {
        return false;
    }
    return true;
}

bool DatabaseManager::tableExists(const std::string &tableName)
{
    // Construct the query to check if the table exists
    std::string query =
        "SELECT name FROM sqlite_master WHERE type='table' AND name='" + tableName + "';";

    // Prepare the SQL statement
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(db, query.c_str(), -1, &stmt, 0);
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        return false;
    }

    // Execute the query
    bool tableExists = false;
    if (sqlite3_step(stmt) == SQLITE_ROW)
    {
        // If there is a row returned, the table exists
        tableExists = true;
    }

    // Finalize the statement to release resources
    sqlite3_finalize(stmt);
    return tableExists;
}

void DatabaseManager::closeDatabase()
{
    if (db != nullptr)
    {
        sqlite3_close(db);
        db = nullptr;
    }
}

void DatabaseManager::executeQuery(const std::string &query)
{
    // errror handeling
    if (db == nullptr)
    {
        throw std::runtime_error("No database connection. Please connect to a database first.");
    }
    // exeute query
    int rc = sqlite3_exec(db, query.c_str(), 0, 0, 0);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }
}

void DatabaseManager::insertTable(const std::string &tableName, const std::string &data)
{
    // construct the SQL INSERT statement
    std::string query = "INSERT OR REPLACE INTO " + tableName + " VALUES (" + data + ");";
    // execute query
    executeQuery(query);
}

void DatabaseManager::showTable(const std::string &tableName)
{
    // construct the SQL statment
    std::string query = "SELECT * FROM " + tableName;
    // errror handeling
    if (db == nullptr)
    {
        throw std::runtime_error("No database connection. Please connect to a database first.");
    }
    if (tableExists(tableName) == false)
    {
        throw std::runtime_error("Table doesn't exist");
    }
    // exeute query
    int rc = sqlite3_exec(db, query.c_str(), print, 0, 0);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }
}

std::vector<Item_user> DatabaseManager::get_user_items(const std::string &user_id)
{
    // construct the SQL statement
    std::string query = "SELECT user_items.item_name, user_items.amount, items.price FROM user_items "
                        "JOIN items ON user_items.item_name = items.item_name "
                        "WHERE user_items.user_id = '" +
                        user_id + "'";
    // shared ptr to a vector which stores the items and their amount
    std::shared_ptr<std::vector<Item_user>> item_list = std::make_shared<std::vector<Item_user>>();
    // execute query
    int rc = sqlite3_exec(db, query.c_str(), safe_user_items, &item_list, 0);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }

    // return the item_list of the user
    return *item_list;
}

std::string DatabaseManager::get_userid(const std::string &username)
{
    // Construct the query to retrieve the user ID based on the username
    std::string query = "SELECT user_id FROM user WHERE username = '" + username + "';";
    // shared ptr to a string which stores the user_id
    std::shared_ptr<std::string> user_id = std::make_shared<std::string>();
    // Execute the query and pass the user_id shared ptr to the callback function
    int rc = sqlite3_exec(db, query.c_str(), safe_user_id, &user_id, nullptr);
    // Error handling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }

    // Return the user_id
    return *user_id;
}

User DatabaseManager::get_user(const std::string &user_id)
{
    // construct the SQL statement
    std::string query = "SELECT username, balance FROM user WHERE user_id = '" + user_id + "';";
    // shared ptr to User which stores the user's name and balance
    std::shared_ptr<User> resultData = std::make_shared<User>();
    // Execute the query and pass the user shared ptr to the callbakc function
    int rc = sqlite3_exec(db, query.c_str(), safe_user, &resultData, nullptr);
    // Error handling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }

    // Return the user_id
    return *resultData;
}

std::vector<Item> DatabaseManager::get_items()
{
    // construct the SQL statement
    std::string query = "SELECT item_name, price FROM items";
    // shared ptr to a vector which stores the items and their amount
    std::shared_ptr<std::vector<Item>> item_list = std::make_shared<std::vector<Item>>();
    // execute query
    int rc = sqlite3_exec(db, query.c_str(), safe_items, &item_list, 0);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }
    // returns the item_list
    return *item_list;
}

void DatabaseManager::buy(int amount, const std::string &itemName, const std::string &user_id)
{   
    // Retrieve the current amount
    std::string getAmountQuery =
        "SELECT amount FROM user_items WHERE item_name = '" + itemName + "' AND user_id = '" + user_id + "';";

    // Construct the INSERT query
    std::string insertItemsQuery =
        "INSERT INTO user_items (item_name, amount, user_id) "
        "VALUES ('" +
        itemName + "', " + std::to_string(amount) + ", '" + user_id + "');";

    // Construct the UPDATE query
    std::string updateItemsQuery =
        "UPDATE user_items SET amount = " + std::to_string(amount) +
        " WHERE item_name = '" + itemName + "' AND user_id = '" + user_id + "';";

    std::string updateBalanceQuery =
        "UPDATE user SET balance = balance - (" +
        std::to_string(amount) + " * (SELECT price FROM items WHERE item_name = '" +
        itemName + "')) WHERE user_id = '" + user_id + "';";

    // shared ptr to a int which stores the current amnount
    std::shared_ptr<User_amount> currentAmount;
    // execute query 
    int rc = sqlite3_exec(db, getAmountQuery.c_str(), safe_amount, &currentAmount, 0);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }

    // Decide whether to perform an INSERT or UPDATE
    std::string query;

    auto anzahl = *currentAmount;  

    if (anzahl.amount > 0)
    {
        query = updateItemsQuery;
    }
    else 
    {
        query = insertItemsQuery;
    }
    // Execute the appropriate query's
    executeQuery(query);
    executeQuery(updateBalanceQuery);
}

void DatabaseManager::sell(int amount, const std::string &itemName, const std::string &user_id)
{
    // need to add an if statment so that someone cant sell more than he actually has
    /* here
    !
    !!!!!!!!!!!!!!!!!!!!!!
    !
    !
    */
    // construct the SQL queries
    std::string updateItemsQuery =
        "UPDATE user_items SET amount = amount - " + std::to_string(amount) +
        " WHERE item_name = '" + itemName + "' AND user_id = '" + user_id + "';";

    std::string updateBalanceQuery =
        "UPDATE user SET balance = balance + (" +
        std::to_string(amount) + " * (SELECT price FROM items WHERE item_name = '" +
        itemName + "')) WHERE user_id = '" + user_id + "';";

    // the balance to be added is the amount * price (of the sold item)
    // execute the queries
    executeQuery(updateItemsQuery);
    executeQuery(updateBalanceQuery);
}

void DatabaseManager::add_account(std::string username, std::string password)
{
    // check if username alreay exists
    if (username_exists(username))
    {
        std::cerr << "Username already exists choose a diffrent username" << std::endl;
        return;
    }
    // generate user uuid
    boost::uuids::uuid userID = boost::uuids::random_generator()();
    // convert to string
    std::string user_id = boost::uuids::to_string(userID);

    // construct query
    std::string query = "INSERT INTO user (user_id, username, password) "
                        "VALUES ('" +
                        user_id + "', '" + username + "', '" + password + "');";

    // execute query
    executeQuery(query);
}

bool DatabaseManager::authenticate_account(std::string username, std::string password)
{
    // Construct the SQL query
    std::string query =
        "SELECT EXISTS(SELECT 1 FROM user WHERE username = '" + username + "' AND password = '" + password + "')";

    int result = 0;
    // Execute the query
    int rc = sqlite3_exec(db, query.c_str(), exists, &result, 0);

    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to execute query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }

    // Check the result
    return (result > 0);
}

void DatabaseManager::pay_in(std::string user_id, int amount)
{
    // construct the SQL query
    std::string query =
        "UPDATE user SET balance = balance + " + std::to_string(amount) + " WHERE user_id = '" + user_id + "';";

    // execute query
    executeQuery(query);
}

void DatabaseManager::pay_out(std::string user_id, int amount)
{
    // construct the SQL query
    std::string query =
        "UPDATE user SET balance = balance - " + std::to_string(amount) + " WHERE user_id = '" + user_id + "';";
    /*
    !!!!!!!!!! need to check if he isnt pulling out more than he has !!!!!!!!!!!!
    */
    // execute query
    executeQuery(query);
}

void DatabaseManager::remove_account(std::string username, std::string password)
{
    // construct query
    std::string query =
        "DELETE FROM user WHERE username = '" + username + "' AND password = '" + password + "';";
    // execute query
    executeQuery(query);
}

void DatabaseManager::add_new_item(const std::string &itemName)
{
    insertTable("items", " '" + itemName + "',0,0,0,0");
}

void DatabaseManager::set_price_stats(std::string item_name, int start_value)
{
    std::random_device rd;                          // seed for the random number generator
    std::mt19937 gen(rd());                         // mersenne twiseter engine for random numbers
    std::uniform_real_distribution<> dis(0.0, 1.0); // Uniform distro between 0 and 1
    float start = std::abs(std::round(start_value * (2 * dis(gen) - 1)));
    float drift = 1.3 * (2 * dis(gen) - 1);
    float standard_deviation = 20;
    // construct query
    std::string query =
        "UPDATE items SET price = " + std::to_string(start) +
        ", tendence = " + std::to_string(drift) +
        ", standard_deviation = " + std::to_string(standard_deviation) +
        " WHERE item_name = '" + item_name + "';";
    // execute query
    executeQuery(query);
}

void DatabaseManager::update_price(std::string itemName)
{
    float dt = 0.001;
    // Construct query
    std::string selectQuery =
        "SELECT tendence, standard_deviation, price FROM items WHERE item_name = '" + itemName + "';";
    // shared ptr to stats which stores tendence, standard_deviation and price
    std::shared_ptr<Stats> resultData = std::make_shared<Stats>();
    // execute query
    int rc = sqlite3_exec(db, selectQuery.c_str(), safe_stats, &resultData, 0);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Error executing query: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to execute query.");
    }
    auto values = *resultData;
    float newPrice = generateRandomWalk_value(values.tendence, values.standard_deviation, dt, values.current_price);
    // Rounding the price to an integer
    int new_price_rounded = std::abs(std::round(newPrice));
    if (new_price_rounded == 0)
        new_price_rounded += 1;
    std::cout << "float newPrice: " << newPrice << " int newPrice: " << new_price_rounded << std::endl;
    // Construct the SQL query
    std::string updateQuery =
        "UPDATE items SET price = " + std::to_string(new_price_rounded) + " WHERE item_name = '" + itemName + "';";
    // execute query
    executeQuery(updateQuery);
}

int DatabaseManager::print(void *data, int column_count, char **column_values, char **column_name)
{
    for (int i = 0; i < column_count; i++)
    {
        // print the column name : column_value (if null we print NULL)
        // if we want to we can change how tables will be printed out
        std::cout << column_name[i] << ": " << (column_values[i] ? column_values[i] : "NULL") << std::endl;
    }
    std::cout << std::endl;
    return 0;
}

int DatabaseManager::safe_user_items(void *data, int column_count, char **column_values, char **column_name)
{
    // lets us get back the pointer item_list which is given through data
    auto item_list = static_cast<std::shared_ptr<std::vector<Item_user>> *>(data);
    // creating a new item object
    Item_user item;
    // assigning members
    item.name = column_values[0] ? column_values[0] : "NULL";
    item.amount = std::stoi(column_values[1] ? column_values[1] : "0"); // std::stoi = string to integer
    item.price = std::stoi(column_values[2] ? column_values[2] : "0");  // std::stoi = string to integer
    // access the vector through the shared pointer and add the item object to it
    (*item_list)->push_back(item);
    return 0;
    // the safe_user_items function gets called for every row thats why it might look confusing but we are getting all items
}

int DatabaseManager::safe_items(void *data, int column_count, char **column_values, char **column_name)
{
    // lets us get back the pointer item_list which is given through data
    auto item_list = static_cast<std::shared_ptr<std::vector<Item>> *>(data);
    // creating a new item object
    Item item;
    // assigning members
    item.name = column_values[0] ? column_values[0] : "NULL";
    item.price = std::stof(column_values[1] ? column_values[1] : "0"); // std::stoi = string to integer
    // access the vector through the shared pointer and add the item object to it
    (*item_list)->push_back(item);
    return 0;
    // the safe_items function gets called for every row thats why it might look confusing but we are getting all items
}

int DatabaseManager::safe_user_id(void *data, int column_count, char **column_values, char **column_name)
{
    // Get the user_id column value
    if (column_count > 0 && column_values[0] != nullptr)
    {
        auto user_id = static_cast<std::shared_ptr<std::string> *>(data);
        **user_id = column_values[0]; // Assign the value to the shared pointer
    }
    return 0;
}

int DatabaseManager::safe_amount(void *data, int column_count, char **column_values, char **column_name)
{
    auto currentAmount = static_cast<std::shared_ptr<User_amount> *>(data);
    // creating a new User_amount object
    User_amount anzahl;
    // assigning members
    anzahl.amount =  std::stoi(column_values[0] ? column_values[0] : "0");
    // assigning the new anzahl/amount to currentAmount
    *currentAmount = std::make_shared<User_amount>(anzahl);
    return 0;
}

int DatabaseManager::safe_user(void *data, int column_count, char **column_values, char **column_name)
{
    auto resultData = static_cast<std::shared_ptr<User> *>(data);
    // creating a new user object
    User user;
    // assigning members
    user.username = column_values[0] ? column_values[0] : "NULL";
    user.balance = std::stof(column_values[1] ? column_values[1] : "0");
    // assigning the new stats to resultData
    *resultData = std::make_shared<User>(user);
    return 0;
}

int DatabaseManager::safe_stats(void *data, int column_count, char **column_values, char **column_name)
{
    auto resultData = static_cast<std::shared_ptr<Stats> *>(data);
    // creating a new stats object
    Stats stats;
    // assigning members
    stats.tendence = std::stof(column_values[0] ? column_values[0] : "0");
    stats.standard_deviation = std::stof(column_values[1] ? column_values[1] : "0");
    stats.current_price = std::stof(column_values[2] ? column_values[2] : "0");
    // assigning the new stats to resultData
    *resultData = std::make_shared<Stats>(stats);
    return 0;
}

int DatabaseManager::exists(void *data, int column_count, char **column_values, char **column_name)
{
    // lets us get back the result from a pointer
    int *result = static_cast<int *>(data);

    if (column_count > 0 && column_values[0] != nullptr)
    {
        *result = std::stoi(column_values[0]);
    }

    return 0;
}

bool DatabaseManager::username_exists(std::string username)
{
    // construct query either returns 0 or 1 represtenting the existence of the username
    std::string checkQuery = "SELECT EXISTS(SELECT 1 FROM user WHERE username = '" + username + "');";

    // prepare the SQL statement
    sqlite3_stmt *stmt;
    int rc = sqlite3_prepare_v2(db, checkQuery.c_str(), -1, &stmt, nullptr);
    // error handeling
    if (rc != SQLITE_OK)
    {
        std::cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << std::endl;
        return false;
    }

    bool exists = false;
    // execute the query
    if (sqlite3_step(stmt) == SQLITE_ROW)
    {
        exists = (sqlite3_column_int(stmt, 0) == 1);
    }

    // finalize the statement to release resources
    sqlite3_finalize(stmt);

    // return result indicating if the username exists
    return exists;
}

float DatabaseManager::generateRandomWalk_value(float tendence, float standard_deviation, float dt, int current_price)
{
    std::random_device rd;                          // seed for the random number generator
    std::mt19937 gen(rd());                         // mersenne twiseter engine for random numbers
    std::uniform_real_distribution<> dis(0.0, 1.0); // Uniform distro between 0 and 1

    float newPrice = 0;
    float sqdt = sqrt(dt);
    float Y = 2 * dis(gen) - 1;

    newPrice = current_price * (1 + tendence * dt + standard_deviation * sqdt * Y);
    return newPrice;
};