from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize
from ClientController import client_controller


class LoginWindow(QMainWindow):

    background_label = None
    main_widget = None
    login_button = None
    cancel_button = None
    username_textfield = None
    password_textfield = None
    font = None
    button_stylesheet = None
    textfield_stylesheet = "background-color: rgba(0, 0, 0, 91); color: white; border: none"
    login_error_label = None

    def initialize_elements(self):
        """!
        initialize_elements is a function which initializes the UI elements of the Window
        """
        self.background_label = QLabel(self)
        self.main_widget = QWidget(self.background_label)
        self.font = QFont("VT323", 14, QFont.Bold)
        self.button_stylesheet = "background-color: rgb(109,109,109);color: white;"
        self.login_button = QPushButton("Login", self.main_widget)
        self.cancel_button = QPushButton("Cancel", self.main_widget)
        self.username_textfield = QLineEdit(self.main_widget)
        self.password_textfield = QLineEdit(self.main_widget)
        self.login_error_label = QLabel(
            "Login error. Connection error or wrong credentials.", self.main_widget)

    def setup_window(self):
        """!
        setup_window is a function which sets the window settings like the dimensions of the window and the its background image or color
        """
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.size())
        self.background_label.setStyleSheet("background-color: rgb(61,44,30);")
        self.background_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.background_label)

    def setup_elements(self):
        """!
        setup_elements is function which sets the UI elements properties like the size, font and stylesheets
        """
        self.login_error_label.setFixedSize(QSize(400, 35))
        self.login_error_label.setFont(self.font)
        self.login_error_label.setStyleSheet("color: red;")
        self.login_error_label.hide()
        self.login_button.setFixedHeight(50)
        self.login_button.setFixedWidth(200)
        self.login_button.setFont(self.font)
        self.login_button.setStyleSheet(self.button_stylesheet)
        self.login_button.clicked.connect(self.login_clicked)
        self.cancel_button.setFixedHeight(50)
        self.cancel_button.setFixedWidth(200)
        self.cancel_button.setFont(self.font)
        self.cancel_button.setStyleSheet(self.button_stylesheet)
        self.cancel_button.clicked.connect(self.cancel_clicked)
        self.username_textfield.setFixedHeight(35)
        self.username_textfield.setFixedWidth(200)
        self.username_textfield.setFont(self.font)
        self.username_textfield.setStyleSheet(self.textfield_stylesheet)
        self.username_textfield.setPlaceholderText("Username")
        self.password_textfield.setFixedHeight(35)
        self.password_textfield.setFixedWidth(200)
        self.password_textfield.setFont(self.font)
        self.password_textfield.setStyleSheet(self.textfield_stylesheet)
        self.password_textfield.setPlaceholderText("Password")
        self.password_textfield.setEchoMode(QLineEdit.Password)

    def position_elements(self):
        """!
        position_elements is function which positions the UI elements correctly
        """
        self.username_textfield.move(300, 235)
        self.password_textfield.move(300, 300)
        self.login_error_label.move(220, 350)
        self.login_button.move(150, 400)
        self.cancel_button.move(450, 400)

    def __init__(self):
        super().__init__()
        self.initialize_elements()
        self.setup_window()
        self.setup_elements()
        self.position_elements()

    def login_clicked(self):
        """!
        login_clicked implements the login button click functionality
        """
        username = self.username_textfield.text()
        password = self.password_textfield.text()
        user_id = client_controller.login(
            username=username, password=password)
        print(user_id)
        if user_id != None:
            import StockmarketWindow
            self.new_window = StockmarketWindow.StockmarketWindow(user_id)
            self.close()
            self.new_window.show()
        else:
            self.login_error_label.show()

    def cancel_clicked(self):
        """!
        cancel_clicked implements the sign up button click functionality
        """
        import TitleScreenWindow
        self.new_window = TitleScreenWindow.TitleScreenWindow()
        self.close()
        self.new_window.show()
