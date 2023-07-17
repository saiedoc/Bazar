#include <iostream>
#include <sqlite3.h>

int main() {
    sqlite3* db;
    int rc = sqlite3_open("database_test.db", &db);
     if (rc != SQLITE_OK) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        throw std::runtime_error("Failed to open database.");
    }
    std::cout<< "working"<< std::endl;
    rc = sqlite3_exec(db,"CREATE TABLE IF NOT EXISTS user ("
        "user_id INTEGER PRIMARY KEY,"
        "username TEXT,"
        "password TEXT,"
        "balance REAL DEFAULT 0.0"
        ");",0,0,0);
}
