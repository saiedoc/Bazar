#include <gtest/gtest.h>
#include <sqlite3.h>
#include <iostream>
#include "database_manager.hpp"
#include <string>

TEST(DatabaseManager, ConnectionTest)
{
    // establish connection
    DatabaseManager data_test("stockmarket_database.db");
    EXPECT_TRUE(data_test.status());
}

TEST(DatabaseManager, DisconnectTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.closeDatabase();
    EXPECT_FALSE(data_test.status());
}

TEST(DatabaseManager, TableExistsTest)
{
    // establish connection
    DatabaseManager data_test("stockmarket_database.db");
    data_test.executeQuery(
        "CREATE TABLE IF NOT EXISTS user ("
        "user_id TEXT PRIMARY KEY,"
        "username TEXT,"
        "password TEXT,"
        "balance INTEGER DEFAULT 0.0"
        ");");

    data_test.executeQuery(
        "CREATE TABLE IF NOT EXISTS user_items ("
        "item_name TEXT,"
        "amount INTEGER DEFAULT 0.0,"
        "user_id TEXT UNIQUE,"
        "FOREIGN KEY (user_id) REFERENCES user (user_id)"
        ");");

    data_test.executeQuery(
        "CREATE TABLE IF NOT EXISTS items ("
        "item_name TEXT PRIMARY KEY,"
        "price INTEGER DEFAULT 0.0,"
        "tendence REAL,"
        "standard_deviation REAL,"
        "start_value REAL"
        ");");
    EXPECT_TRUE(data_test.tableExists("user"));
    EXPECT_TRUE(data_test.tableExists("user_items"));
    EXPECT_TRUE(data_test.tableExists("items"));
}

TEST(DatabaseManager, addAccountTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.add_account("batman", "catwoman");
    data_test.showTable("user");
}

TEST(DatabaseManager, user_idTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    std::string user_id = data_test.get_userid("batman");
    std::cout << user_id << std::endl;
}

TEST(DatabaseManager, authenticateAccountTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    // correct authentication
    EXPECT_TRUE(data_test.authenticate_account("batman", "catwoman"));
    // authentication with wrong password
    EXPECT_FALSE(data_test.authenticate_account("batman", "alfred"));
}

// needs user_id
TEST(DatabaseManager, payIn_and_OutTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.pay_in("4866326d-9024-43d2-bfd0-0ff11ca5f5c9", 100);
    data_test.showTable("user");
    data_test.pay_out("4866326d-9024-43d2-bfd0-0ff11ca5f5c9", 50);
    data_test.showTable("user");
}

TEST(DatabaseManager, insertTableTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.insertTable("items", "'batmobile',10,0,0,0");
    data_test.showTable("items");
}

TEST(DatabaseManager, getItemsTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    auto items = data_test.get_items();
    for (const Item &item : items)
    {
        std::cout << "Name: " << item.name << ", Price: " << item.price << std::endl;
    }
}

// to so that from here everything works too frist build with eveerything below commented
// then get the user_id and uncomment below with the specific user_id

TEST(DatabaseManager, buyItemTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.buy(2, "batmobile", "4866326d-9024-43d2-bfd0-0ff11ca5f5c9");
    data_test.showTable("user");
    data_test.showTable("user_items");
}

TEST(DatabaseManager, sellItemTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.sell(1, "batmobile", "4866326d-9024-43d2-bfd0-0ff11ca5f5c9");
    data_test.showTable("user");
    data_test.showTable("user_items");
}

TEST(DatabaseManager, getUserItemsTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    auto items = data_test.get_user_items("4866326d-9024-43d2-bfd0-0ff11ca5f5c9");
    for (const Item_user &item : items)
    {
        std::cout << "Name: " << item.name << ", Amount: " << item.amount << ", Price: " << item.price << std::endl;
    }
}

TEST(DatabaseManager, setStatsForItemTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.showTable("items");
    data_test.set_price_stats("batmobile", 5);
    data_test.showTable("items");
}

// probably not so gucci
TEST(DatabaseManager, updatePrice00Test)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.showTable("items");
    data_test.update_price("batmobile");
    data_test.showTable("items");
}

// probably not so gucci
TEST(DatabaseManager, updatePrice01Test)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.update_price("batmobile");
    data_test.showTable("items");
}

TEST(DatabaseManager, removeAccountTest)
{
    DatabaseManager data_test("stockmarket_database.db");
    data_test.remove_account("batman", "catwoman");
    data_test.showTable("user");
}
