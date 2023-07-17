from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt


class TitleScreenWindow(QMainWindow):

    background_label = None
    background_pixmap = None
    main_widget = None
    title_label = None
    title_pixmap = None
    login_button = None
    signup_button = None
    font = None
    button_stylesheet = None

    def initialize_elements(self):
        """!
        initialize_elements is a function which initializes the UI elements of the Window
        """
        self.background_label = QLabel(self)
        self.main_widget = QWidget(self.background_label)
        self.title_label = QLabel(self.main_widget)
        self.title_pixmap = QPixmap("./resources/BazarTitle.png")
        self.font = QFont("VT323", 14, QFont.Bold)
        self.button_stylesheet = "background-color: rgb(109,109,109);color: white;"
        self.login_button = QPushButton("Login", self.main_widget)
        self.signup_button = QPushButton("Sign Up", self.main_widget)

    def setup_window(self):
        """!
        setup_window is a function which sets the window settings like the dimensions of the window and the its background image or color
        """
        self.setWindowTitle("Title Screen")
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
        self.title_label.setPixmap(self.title_pixmap)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.login_button.setFixedHeight(50)
        self.login_button.setFixedWidth(200)
        self.login_button.setFont(self.font)
        self.login_button.setStyleSheet(self.button_stylesheet)
        self.login_button.clicked.connect(self.login_clicked)
        self.signup_button.setFixedHeight(50)
        self.signup_button.setFixedWidth(200)
        self.signup_button.setFont(self.font)
        self.signup_button.setStyleSheet(self.button_stylesheet)
        self.signup_button.clicked.connect(self.signup_clicked)

    def position_elements(self):
        """!
        position_elements is function which positions the UI elements correctly
        """
        self.title_label.move(220, 100)
        self.login_button.move(285, 325)
        self.signup_button.move(285, 400)

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
        import LoginWindow
        self.new_window = LoginWindow.LoginWindow()
        self.close()
        self.new_window.show()

    def signup_clicked(self):
        """!
        signup_clicked implements the sign up button click functionality
        """
        import SignUpWindow
        self.new_window = SignUpWindow.SignUpWindow()
        self.close()
        self.new_window.show()
