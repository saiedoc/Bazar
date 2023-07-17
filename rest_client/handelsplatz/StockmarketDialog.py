from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from ClientController import client_controller


class StockMarketWindowDialog(QMainWindow):
    parent_window = None
    dialog_type = None
    background_label = None
    label_text = None
    dialog_label = None
    text_field = None
    text_field_placeholder = None
    left_button = None
    right_button = None
    left_button_text = None
    right_button_text = None
    button_stylesheet = None
    font = None
    main_widget = None
    textfield_stylesheet = "background-color: rgba(0, 0, 0, 91); color: white; border: none"
    item_name = None

    def initialize_elements(self):
        """!
        initialize_elements is a function which initializes the UI elements of the Dialog
        """
        self.background_label = QLabel(self)

        self.font = QFont("VT323", 16, QFont.Bold)
        self.button_stylesheet = "background-color: rgb(109,109,109);color: white;"
        self.main_widget = QWidget(self.background_label)

        if self.dialog_type == "Logout":
            self.left_button_text = "Yes"
            self.right_button_text = "No"
            self.label_text = "Are you sure you want to logout?"
        else:
            self.right_button_text = "Cancel"
            self.text_field_placeholder = "Amount"
            self.text_field = QLineEdit(self.main_widget)
            if self.dialog_type == "Payin":
                self.label_text = "How much do you want to pay in?"
                self.left_button_text = "Payin"
            if self.dialog_type == "Buy":
                self.label_text = "How much do you want to buy?"
                self.left_button_text = "Buy"
            if self.dialog_type == "Sell":
                self.label_text = "How much do you want to sell?"
                self.left_button_text = "Sell"

        self.dialog_label = QLabel(self.label_text, self.main_widget)
        self.left_button = QPushButton(self.left_button_text, self.main_widget)
        self.right_button = QPushButton(
            self.right_button_text, self.main_widget)
        self.setCentralWidget(self.background_label)

    def setup_dialog(self):
        """!
        setup_dialog is a function which sets the window settings like the dimensions of the dialog and the its background image or color
        """
        self.setWindowTitle("Dialog")
        self.setGeometry(100, 100, 600, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.size())
        self.background_label.setStyleSheet("background-color: rgb(61,44,30);")
        self.background_label.setAlignment(Qt.AlignCenter)

    def setup_elements(self):
        """!
        setup_elements is function which sets the UI elements properties like the size, font and stylesheets
        """
        self.dialog_label.setFont(self.font)
        self.dialog_label.setStyleSheet("color: white;")
        self.left_button.setFixedHeight(50)
        self.left_button.setFixedWidth(200)
        self.left_button.setFont(self.font)
        self.left_button.setStyleSheet(self.button_stylesheet)
        self.left_button.clicked.connect(self.left_clicked)
        self.right_button.setFixedHeight(50)
        self.right_button.setFixedWidth(200)
        self.right_button.setFont(self.font)
        self.right_button.setStyleSheet(self.button_stylesheet)
        self.right_button.clicked.connect(self.right_clicked)
        if self.text_field != None:
            self.text_field.setFixedHeight(35)
            self.text_field.setFixedWidth(200)
            self.text_field.setFont(self.font)
            self.text_field.setStyleSheet(self.textfield_stylesheet)
            self.text_field.setPlaceholderText(self.text_field_placeholder)

    def position_elements(self):
        """!
        position_elements is function which positions the UI elements correctly
        """
        self.dialog_label.move(175, 50)
        if self.text_field != None:
            self.text_field.move(200, 120)
        self.left_button.move(75, 200)
        self.right_button.move(330, 200)

    def __init__(self, type, parent_window, bs_item_name):
        super().__init__()
        self.parent_window = parent_window
        self.dialog_type = type
        self.item_name = bs_item_name
        self.initialize_elements()
        self.setup_dialog()
        self.setup_elements()
        self.position_elements()

    def left_clicked(self):
        """!
        left_clicked function implements the Payin, Buy and Sell of each dialog respectively
        """
        if self.dialog_type == "Logout":
            import subprocess
            self.close()
            self.parent_window.close()
            script_path = 'main.py'
            subprocess.call(['python', script_path])
            QApplication.exit()

        elif self.dialog_type == "Payout":
            client_controller.pay_out(
                self.parent_window.user_id, int(self.text_field.text()))
            self.close()
        elif self.dialog_type == "Payin":
            client_controller.pay_in(
                self.parent_window.user_id, int(self.text_field.text()))
            self.close()
        elif self.dialog_type == "Buy":
            client_controller.buy(
                int(self.text_field.text()), self.item_name, self.parent_window.user_id)
            self.close()
        else:
            client_controller.sell(
                int(self.text_field.text()), self.item_name, self.parent_window.user_id)
            self.close()

    def right_clicked(self):
        """!
        cancel_clicked closes the dialog
        """
        self.close()
