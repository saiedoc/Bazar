import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontDatabase
from TitleScreenWindow import TitleScreenWindow
from ClientController import client_controller

if __name__ == "__main__":
    app = QApplication(sys.argv)
    font_path = os.path.abspath("./resources/VT323-Regular.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    window = TitleScreenWindow()
    window.show()
    sys.exit(app.exec_())
