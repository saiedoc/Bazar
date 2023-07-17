## Konfiguration des Buildsystems CMake ##

# Minimale Version des Buildsystems
cmake_minimum_required(VERSION 3.14)
# Name des Projekts
project(Bazar)

## Optionen ##

# Setzte verwendeten C++-Standard auf C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Prüfe ob Heapspeicher gefunden wird,
# der nicht freigegeben wurde
# add_compile_options(-fsanitize=address, -v)
# add_link_options(-fsanitize=address)
add_link_options(-lsqlite3)

# Füge selbsgeschriebene Includes hinzu
include_directories(include)
# Füge externe Includes hinzu
include_directories(external)


#----------------------------------------------#
#---------------Verwende Boost-----------------#
#----------------------------------------------#

find_package(Boost REQUIRED)

#----------------------------------------------#
#---------------Verwende SQLite3---------------#
#----------------------------------------------#

find_package(SQLite3 REQUIRED) 

#----------------------------------------------#
#---------------Verwende Pybind11--------------#
#----------------------------------------------#

find_package(pybind11 REQUIRED)

#----------------------------------------------#
#----------Download and use GoogleTest---------#
#----------------------------------------------#

# Use CMakes FetchContent
include(FetchContent)
# Workaround for CMake >= 3.24
# Avoid warning about DOWNLOAD_EXTRACT_TIMESTAMP
if (CMAKE_VERSION VERSION_GREATER_EQUAL "3.24.0")
  cmake_policy(SET CMP0135 NEW)
endif()

# Download GoogleTest (we use version 1.12.1)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# Workaround for Windows:
# Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Include CMake configuration of GoogleTest
FetchContent_MakeAvailable(googletest)
include(GoogleTest)

# Enable GoogleTest
enable_testing()


#----------------------------------------------#
#---------------Erzeuge Projekt----------------#
#----------------------------------------------#
# Legt die Variable SRC_FILES an, die alle
# .cpp-Dateien des Projekts benennt,
# die in Verzeichnis src/ liegen.
file(GLOB SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)

#add_executable(demo_qt_1
#    examples/demo_qt_1.cpp
#)

add_executable(demo_sqlite
    examples/demo_sqlite.cpp
    src/database_manager.cpp
)

add_executable(stockmarket_database
    database/stockmarket_database.cpp
)
target_link_libraries(stockmarket_database 
  PRIVATE
  SQLite::SQLite3
)

# Baue pybind11-Schnittstelle
pybind11_add_module(database_manager
  examples/demo_database_manager.cpp
  ${SRC_FILES}
)


# Specify the output name of the module
set_target_properties(database_manager PROPERTIES OUTPUT_NAME "database_manager")

# Link necessary libraries
target_link_libraries(database_manager PRIVATE SQLite::SQLite3)
target_link_libraries(demo_sqlite PRIVATE SQLite::SQLite3)

# Specify the desired location for the built module
set_target_properties( PROPERTIES LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")

#----------------------------------------------#
#----------Installation des Projekts-----------#
#----------------------------------------------#

# Pybind11 shared library erstellen für database_manager
install(TARGETS database_manager
  COMPONENT python
  LIBRARY DESTINATION "${PROJECT_SOURCE_DIR}/extra")

#----------------------------------------------#
#---------Erzeuge Google Testprogramme---------#
#----------------------------------------------#

# Declare test program database_manger_tes
add_executable(database_manager_test tests/database_manager_test.cpp ${SRC_FILES})
target_link_libraries(database_manager_test GTest::gtest_main SQLite::SQLite3)
gtest_discover_tests(database_manager_test)
