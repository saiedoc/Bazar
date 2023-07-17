# Bazar 

## Description
This project implements our version of a stock market "bazar" <br>
Bazar allows us to buy and sell minecraft items. <br>

## Stock market classes:
- open [documentation](html/index.html) to get to our explicit class and module descriptions. <br>


## Installation
- clang >= 13.0 
- cmake >= 3.16
- Boost >=1.82.0 for C++
- SQLite3 >= 3.3 for C++
    - 
    ```
    sudo apt-get install sqlite3 libsqlite3-dev
    ```
- python3 >= 3.8
    - python3-pip3 >= 10
    - python3-dev und python3-pybind11
    - Python3-Module (via pip3): pybind11, pyside6 sowie fastapi[all]
    - PyQt5


## GUI Design

To check the UI design in figma follow the link: <br>
https://www.figma.com/file/wRSnqXSSI0EaEr3yk4b94c/Bazar?type=design&node-id=0%3A1&mode=design&t=v5SeHBSRplECaXF6-1

## Build
To build the project write following command (for Linux and MacOS)
```
cmake -S . -B build && cmake --build build && cmake --install build
```

## Usage
Run both files to set up the server and client.
- /handelsplatz/rest_server/main.py
- /handelsplatz/rest_client/main.py <br>
In the terminal write follwing code, but make sure to be in the right directory 
```
python3 main.py
```
## Support
Contact me at "saeidaussi@outlook.com"

## Authors and acknowledgment
- [Leon](https://gitlab.informatik.uni-bonn.de/peplaul0) - Developer, Tester
- [Saied](https://gitlab.informatik.uni-bonn.de/aussis0) - Developer, Tester
- [Zita](https://gitlab.informatik.uni-bonn.de/aratoz0) - Developer, Tester

## License
This project is licensed under the [MIT License](LICENSE).<br>
All the textures, icons and other elements that were needed to implement the UI belong to Mojang and their artists. <br>
This project was developed for educational purposes only.

## Project status
Development stopped
