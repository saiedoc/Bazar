#include "database_manager.hpp"
#include <sqlite3.h>
#include "../src/database_manager.cpp" // needs to be includes otherwise "Undefined symbols for architecture arm64" error

int main()
{
    // establish connection
    DatabaseManager stock_database("stockmarket_database.db");

    // Perform database operations using the db object
    // make user table
    stock_database.executeQuery(
        "CREATE TABLE IF NOT EXISTS user ("
        "user_id TEXT PRIMARY KEY,"
        "username TEXT,"
        "password TEXT,"
        "balance INTEGER DEFAULT 0.0"
        ");");

    // make user_items table
    stock_database.executeQuery(
        "CREATE TABLE IF NOT EXISTS user_items ("
        "item_name TEXT,"
        "amount INTEGER DEFAULT 0.0,"
        "user_id TEXT,"
        "FOREIGN KEY (item_name) REFERENCES item (item_name),"
        "FOREIGN KEY (user_id) REFERENCES user (user_id),"
        "PRIMARY KEY (user_id,item_name)"
        ");");

    // make item table
    stock_database.executeQuery(
        "CREATE TABLE IF NOT EXISTS items ("
        "item_name TEXT PRIMARY KEY,"
        "price INTEGER DEFAULT 0.0,"
        "tendence REAL,"
        "standard_deviation REAL,"
        "start_value REAL"
        ");");

    /*
    //------ this is just for testing -------
    // testing if tables exist
    std::cout << "table exists: "<<stock_database.tableExists("user") <<std::endl;

    //
    stock_database.add_account("test","password");

    // printing table
    stock_database.showTable("user");


    // inserting item
    stock_database.insertTable("items","'batmobile',10,0,0,0");
    stock_database.set_price_stats("batmobile");
    stock_database.showTable("items");
    stock_database.update_price("batmobile");
    stock_database.showTable("items");

    // Close the database connection when done
    */
    stock_database.closeDatabase();
    std::cout << "working" << std::endl;
    return 0;
}
