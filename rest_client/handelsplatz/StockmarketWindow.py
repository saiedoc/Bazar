import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QSize, QTimer
import pyqtgraph as pg
from StockmarketDatabinder import StockmarketDatabinder


class StockmarketWindow(QMainWindow):
    background_label = None
    payin_button = None
    main_widget = None
    logout_button = None
    balance_label = None
    items_list_label = None
    switch_button = None
    items_list = None
    items_list_scrollarea = None
    chart_view = None
    item_price_label = None
    emerald_icon1 = None
    buy_label = None
    sell_label = None
    buy_button = None
    sell_button = None
    selected_item = 'Diamond'
    displayed_items = []
    chart_widget = None
    user_id = None
    user_amount_label = None
    all_items_dict = {}
    my_items_dict = {}
    user_balance = 0

    def initialize_elements(self):
        """!
        initialize_elements is a function which initializes the UI elements of the Window
        """
        self.background_label = QLabel(self)
        self.main_widget = QWidget(self.background_label)
        self.font = QFont("VT323", 16, QFont.Bold)
        self.all_items_dict = StockmarketDatabinder.get_all_items(
            self.all_items_dict)
        # self.my_items_dict = StockmarketDatabinder.get_user_items(self.my_items_dict,self.user_id)
        self.displayed_items = self.all_items_dict.keys()
        self.button_stylesheet = "background-color: rgb(109,109,109); color: white;"
        self.list_button_stylesheet = "background-color:  rgb(109,109,109); color: white;text-align:left; padding-left:20px;"
        self.items_list_scrollarea_stylesheet = "background-color: rgba(0, 0, 0, 100);"
        self.label_stylesheet = "color: white;"
        self.logout_button = QPushButton("", self.main_widget)
        self.balance_label = QLabel("Username Balance: 0", self.main_widget)
        self.emerald_icon1 = QLabel(self.main_widget)
        self.payin_button = QPushButton("", self.main_widget)
        self.items_list_label = QLabel("My Items", self.main_widget)
        self.switch_button = QPushButton("", self.main_widget)
        self.items_list_scrollarea = QScrollArea(self.main_widget)
        self.items_list = QVBoxLayout(self.items_list_scrollarea)
        self.item_price_label = QLabel("", self.main_widget)
        self.buy_label = QLabel("Buy", self.main_widget)
        self.buy_button = QPushButton("", self.main_widget)
        self.sell_label = QLabel("Sell", self.main_widget)
        self.sell_button = QPushButton("", self.main_widget)
        self.user_amount_label = QLabel("Your Amount: 0", self.main_widget)

    def setup_elements(self):
        """!
        setup_elements is function which sets the UI elements properties like the size, font and stylesheets
        """
        self.logout_button.setFixedHeight(50)
        self.logout_button.setFixedWidth(50)
        self.logout_button.setFont(self.font)
        self.logout_button.setIcon(QIcon("./resources/LogOut Icon.png"))
        self.logout_button.setStyleSheet(self.button_stylesheet)
        self.logout_button.clicked.connect(self.logout_button_clicked)

        self.balance_label.setStyleSheet(self.label_stylesheet)
        self.balance_label.setFont(self.font)

        self.emerald_icon1.setPixmap(QPixmap("./resources/Emerald.png"))
        self.emerald_icon1.setFixedSize(QSize(26, 26))

        self.payin_button.setIcon(QIcon("./resources/PayOut Icon.png"))
        self.payin_button.setStyleSheet(self.button_stylesheet)
        self.payin_button.clicked.connect(self.payin_button_clicked)

        self.items_list_label.setStyleSheet(self.label_stylesheet)
        self.items_list_label.setFont(self.font)

        self.switch_button.setFont(self.font)
        self.switch_button.setStyleSheet(self.button_stylesheet)
        self.switch_button.setIcon(QIcon("./resources/Switch Icon.png"))
        self.switch_button.clicked.connect(self.switch_button_clicked)

        self.item_price_label.setFixedWidth(300)
        self.item_price_label.setStyleSheet(self.label_stylesheet)
        self.item_price_label.setFont(self.font)

        self.buy_label.setStyleSheet(self.label_stylesheet)
        self.buy_label.setFont(self.font)

        self.sell_label.setStyleSheet(self.label_stylesheet)
        self.sell_label.setFont(self.font)

        self.user_amount_label.setFixedWidth(300)
        self.user_amount_label.setStyleSheet(self.label_stylesheet)
        self.user_amount_label.setFont(self.font)

        self.buy_button.setIcon(QIcon("./resources/Buy Icon.png"))
        self.buy_button.setStyleSheet(self.button_stylesheet)
        self.buy_button.clicked.connect(self.buy_button_clicked)

        self.sell_button.setIcon(QIcon("./resources/Sell Icon.png"))
        self.sell_button.setStyleSheet(self.button_stylesheet)
        self.sell_button.clicked.connect(self.sell_button_clicked)

        self.populate_items_list(self.displayed_items)

        self.setStyleSheet("background-color: transparent;")

    def position_elements(self):
        """!
        position_elements is function which positions the UI elements correctly
        """
        self.logout_button.move(720, 20)
        self.balance_label.move(20, 20)
        self.emerald_icon1.move(210, 18)
        self.payin_button.move(240, 20)
        self.items_list_label.move(20, 80)
        self.switch_button.move(240, 80)
        self.items_list_scrollarea.setGeometry(20, 130, 250, 400)
        self.item_price_label.move(300, 510)
        self.user_amount_label.move(300, 550)
        self.buy_label.move(570, 510)
        self.buy_button.move(610, 510)
        self.sell_label.move(650, 510)
        self.sell_button.move(700, 510)

    def setup_window(self):
        """!
        setup_window is a function which sets the window settings like the dimensions of the window and the its background image or color
        """
        self.setWindowTitle("Stock Market")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.setFixedSize(self.size())
        self.background_label.setStyleSheet("background-color: rgb(61,44,30);")
        self.background_label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.background_label)

    def populate_items_list(self, itemslist):
        """!
        populates the items list with either the users items or all available to buy items
        """
        for item in itemslist:
            button = QPushButton(item, self.background_label)
            button.setFixedWidth(220)
            button.setFixedHeight(50)
            button.setStyleSheet(self.list_button_stylesheet)
            button.setFont(self.font)
            button.setIcon(QIcon("./resources/"+item+".png"))
            button.setIconSize(QSize(50, 25))
            button.clicked.connect(self.select_list_item)
            self.items_list.addWidget(button)
        self.items_list.addStretch(1)

    def clear_items_list(self):
        """!
        clears the items list in order to repopulate it with the appropraite items list
        """
        while self.items_list.count():
            item = self.items_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def buy_button_clicked(self):
        """!
        event function which opens the buy item dialog.
        """
        import StockmarketDialog
        self.buy_dialog = StockmarketDialog.StockMarketWindowDialog(
            "Buy", self, self.selected_item)
        self.buy_dialog.show()

    def sell_button_clicked(self):
        """!
        event function which opens the sell item dialog.
        """
        import StockmarketDialog
        self.sell_dialog = StockmarketDialog.StockMarketWindowDialog(
            "Sell", self, self.selected_item)
        self.sell_dialog.show()

    def payin_button_clicked(self):
        """!
        event function which opens the payin dialog.
        """
        import StockmarketDialog
        self.payin_dialog = StockmarketDialog.StockMarketWindowDialog(
            "Payin", self, None)
        self.payin_dialog.show()

    def logout_button_clicked(self):
        """!
        event function which opens the logout dialog.
        """
        import StockmarketDialog
        self.logout_dialog = StockmarketDialog.StockMarketWindowDialog(
            "Logout", self, None)
        self.logout_dialog.show()

    def switch_button_clicked(self):
        """!
        event function implements the functionality that allows the user to switch the view from my items to all items and vice versa
        """
        if self.displayed_items == self.all_items_dict.keys():
            self.clear_items_list()
            # self.my_items_dict = StockmarketDatabinder.get_user_items(
            #     self.my_items_dict, self.user_id)
            self.displayed_items = self.my_items_dict.keys()
            self.items_list_label.setText("My Items")
            self.populate_items_list(self.displayed_items)
        else:
            self.clear_items_list()
            # self.all_items_dict = StockmarketDatabinder.get_all_items(
            #     self.all_items_dict)
            self.displayed_items = self.all_items_dict.keys()
            self.items_list_label.setText("All Items")
            self.populate_items_list(self.displayed_items)

    def update_amount_price_label(self):
        """!
        a function that updates the item's price label in the interface and the amount of this item that the uses has.
        """
        if self.selected_item == "Amethyst":
            self.item_price_label.setText(
                "Amethyst current price: " + str(self.all_items_dict["Amethyst"][len(self.all_items_dict["Amethyst"])-1]))
        if self.selected_item == "Diamond":
            self.item_price_label.setText(
                "Diamond current price: " + str(self.all_items_dict["Diamond"][len(self.all_items_dict["Diamond"])-1]))
        if self.selected_item == "Gold":
            self.item_price_label.setText(
                "Gold current price: " + str(self.all_items_dict["Gold"][len(self.all_items_dict["Gold"])-1]))
        if self.selected_item == "Iron":
            self.item_price_label.setText(
                "Iron current price: " + str(self.all_items_dict["Iron"][len(self.all_items_dict["Iron"])-1]))
        if self.selected_item == "Lapis Lazuli":
            self.item_price_label.setText(
                "Lapis Lazuli current price: " + str(self.all_items_dict["Lapis Lazuli"][len(self.all_items_dict["Lapis Lazuli"])-1]))
        if self.selected_item == "Netherite":
            self.item_price_label.setText(
                "Netherite current price: " + str(self.all_items_dict["Netherite"][len(self.all_items_dict["Netherite"])-1]))
        if self.selected_item == "Redstone":
            self.item_price_label.setText(
                "Redstone current price: " + str(self.all_items_dict["Redstone"][len(self.all_items_dict["Redstone"])-1]))
        if self.selected_item in self.my_items_dict.keys():
            self.user_amount_label.setText(
                "Your Amount: " + str(self.my_items_dict[self.selected_item]))
        else:
            self.user_amount_label.setText("Your Amount: 0")

    def select_list_item(self):
        button_text = self.sender().text()
        self.selected_item = button_text

    def setup_chart(self):
        """!
        a function that sets up the charts layout, properties and appearence.
        """
        self.chart_widget = QWidget(self.main_widget)
        self.chart_view = QVBoxLayout(self.chart_widget)
        self.chart_item = pg.PlotWidget()
        self.chart_item.plotItem.getViewBox().setMouseEnabled(False, False)
        # self.chart_item.plotItem.addLegend()
        self.hours = [1]
        self.amethyst_pen = pg.mkPen(color=(207, 160, 243), width=3)
        self.diamond_pen = pg.mkPen(color=(85, 239, 219), width=3)
        self.gold_pen = pg.mkPen(color=(235, 245, 95), width=3)
        self.iron_pen = pg.mkPen(color=(216, 216, 216), width=3)
        self.lapis_lazuli_pen = pg.mkPen(color=(60, 107, 193), width=3)
        self.netherite_pen = pg.mkPen(color=(77, 73, 77), width=3)
        self.redstone_pen = pg.mkPen(color=(245, 1, 0), width=3)
        styles = {'color': 'white', 'font-size': '15px'}
        self.chart_item.plotItem.setLabel('left', 'Price', **styles)
        self.chart_item.plotItem.setLabel('bottom', 'Hour', **styles)
        self.chart_item.setBackground((0, 0, 0, 70))
        self.chart_view.addWidget(self.chart_item)
        self.chart_widget.setGeometry(250, 110, 550, 400)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        """!
        a function responsible for populating the chart with the appropiate data and plotting it and also updates user and items data.
        """
        self.timer.stop()
        self.all_items_dict = StockmarketDatabinder.get_all_items(
            self.all_items_dict)

        self.my_items_dict = StockmarketDatabinder.get_user_items(
            self.my_items_dict, self.user_id)

        self.user_data = StockmarketDatabinder.get_user_data(self.user_id)

        StockmarketDatabinder.update_prices()
        self.timer.start()
        MAX_POINTS = 30
        if len(self.hours) != 0:
            x = self.hours[len(self.hours) - 1] + 1
        else:
            x = 1
        self.hours.append(x)

        self.user_balance = self.user_data['balance']
        self.username = self.user_data['username']

        self.balance_label.setText(
            self.username + " Balance: " + str(self.user_balance))

        if len(self.hours) > MAX_POINTS:
            self.hours = self.hours[-MAX_POINTS:]
            self.all_items_dict["Amethyst"] = self.all_items_dict["Amethyst"][-MAX_POINTS:]
            self.all_items_dict["Diamond"] = self.all_items_dict["Diamond"][-MAX_POINTS:]
            self.all_items_dict["Gold"] = self.all_items_dict["Gold"][-MAX_POINTS:]
            self.all_items_dict["Iron"] = self.all_items_dict["Iron"][-MAX_POINTS:]
            self.all_items_dict["Lapis Lazuli"] = self.all_items_dict["Lapis Lazuli"][-MAX_POINTS:]
            self.all_items_dict["Netherite"] = self.all_items_dict["Netherite"][-MAX_POINTS:]
            self.all_items_dict["Redstone"] = self.all_items_dict["Redstone"][-MAX_POINTS:]

        self.chart_item.plotItem.clear()
        if "Amethyst" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Amethyst"], pen=self.amethyst_pen, name="Athemyst")
        if "Diamond" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Diamond"], pen=self.diamond_pen, name="Diamond")
        if "Gold" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Gold"], pen=self.gold_pen, name="Gold")
        if "Iron" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Iron"], pen=self.iron_pen, name="Iron")
        if "Lapis Lazuli" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Lapis Lazuli"], pen=self.lapis_lazuli_pen, name="Lapis Lazuli")
        if "Netherite" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Netherite"], pen=self.netherite_pen, name="Netherite")
        if "Redstone" in self.displayed_items:
            self.chart_item.plotItem.plot(
                self.hours, self.all_items_dict["Redstone"], pen=self.redstone_pen, name="Redstone")

        self.update_amount_price_label()

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initialize_elements()
        self.setup_window()
        self.setup_elements()
        self.position_elements()
        self.setup_chart()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockmarketWindow()
    window.show()
    sys.exit(app.exec_())
