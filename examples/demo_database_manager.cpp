#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <database_manager.hpp>

namespace py = pybind11;

PYBIND11_MODULE(database_manager, m) {
    
    m.doc() = "database_manager for further informations on how these functions work look into the documentation of DatabaseManager.";

    py::class_<Item>(m, "Item")
        .def(py::init<>())
        .def_readwrite("name", &Item::name)
        .def_readwrite("price", &Item::price);
    
    py::class_<User_amount>(m, "User_amount")
        .def(py::init<>())
        .def_readwrite("amount", &User_amount::amount);

    py::class_<Item_user>(m, "ItemUser")
        .def(py::init<>())
        .def_readwrite("name", &Item_user::name)
        .def_readwrite("amount", &Item_user::amount);
    
    py::class_<User>(m, "User")
        .def(py::init<>())
        .def_readwrite("name", &User::username)
        .def_readwrite("amount", &User::balance);

    py::class_<Stats>(m, "Stats")
        .def(py::init<>())
        .def_readwrite("tendence", &Stats::tendence)
        .def_readwrite("standard_deviation", &Stats::standard_deviation)
        .def_readwrite("current_price", &Stats::current_price);

    py::class_<DatabaseManager>(m, "DatabaseManager")
        .def(py::init<const std::string&>(),
        "Constructs a new DatabaseManager object and establishes a connection to the specified database.")

        .def("connect", &DatabaseManager::connect, 
        "Connects to the specified database.")

        .def("status", &DatabaseManager::status,
        "Status of connection")
        
        .def("tableExists", &DatabaseManager::tableExists,
        "Check if a specific table exists.")

        .def("closeDatabase", &DatabaseManager::closeDatabase, 
        "Closes the database connection.")

        .def("executeQuery", &DatabaseManager::executeQuery, 
        "Executes the specified SQL query on the connected database.")

        .def("insertTable", &DatabaseManager::insertTable, 
        "Inserts data into the specified table from the connected database.")

        .def("showTable", &DatabaseManager::showTable, 
        "Prints the specified table.")

        .def("get_user_items", &DatabaseManager::get_user_items, 
        "Retrieves the items and their amounts for a specific user from the database.")

        .def("get_items", &DatabaseManager::get_items, 
        "Retrieves all items and their prices from the database.")

        .def("get_user", &DatabaseManager::get_user)
        
        .def("get_userid", &DatabaseManager::get_userid)

        .def("buy", &DatabaseManager::buy, 
        "Buys a specified amount of an item for a user.")

        .def("sell", &DatabaseManager::sell, 
        "Sells a specified amount of an item by updating the item's amount in the user_items table.")

        .def("add_account", &DatabaseManager::add_account, 
        "Adds a new user account with the provided username and password.")

        .def("authenticate_account", &DatabaseManager::authenticate_account, 
        "Authenticates a user account with the provided username and password.")
        
        .def("pay_in", &DatabaseManager::pay_in, 
        "Adds cash to a user's balance.")

        .def("pay_out", &DatabaseManager::pay_out, 
        "Withdraws cash from a user's balance.")

        .def("remove_account", &DatabaseManager::remove_account, 
        "Removes a user account from the database.")

        .def("add_new_item", &DatabaseManager::add_new_item)

        .def("set_price_stats", &DatabaseManager::set_price_stats, 
        "Sets the values of an Item and generates a course.")

        .def("update_price", &DatabaseManager::update_price, 
        "Updates the prices in the items table for the specified item");

}


