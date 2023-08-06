from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
# from PyQt5.QtCore import QTimer
# from server.statistic import StatWindow
from config_window import ConfigWindow


class MainWindow(QMainWindow):
    """Main window of server"""

    def __init__(self, database, config):
        super().__init__()

        self.database = database

        self.config = config

        self.exitAction = QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.triggered.connect(qApp.quit)

        self.refresh_button = QAction('Update list', self)

        self.config_btn = QAction('Server setting', self)

        # self.show_history_button = QAction('User history', self)

        self.statusBar()
        self.statusBar().showMessage('Server Working')

        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(self.exitAction)
        self.toolbar.addAction(self.refresh_button)
        # self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)

        self.setFixedSize(800, 600)
        self.setWindowTitle('Messaging Server alpha release')

        self.label = QLabel('User connection list:', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.active_clients_table = QTableView(self)
        self.active_clients_table.move(10, 45)
        self.active_clients_table.setFixedSize(780, 400)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.create_users_model)
        # self.timer.start(1000)

        self.refresh_button.triggered.connect(self.create_users_model)
        # self.show_history_button.triggered.connect(self.show_statistics)
        self.config_btn.triggered.connect(self.server_config)

        self.show()

    def create_users_model(self):
        """The method that fills is a table of active users."""

        list_users = self.database.active_users_list()
        user_list = QStandardItemModel()
        user_list.setHorizontalHeaderLabels(
            ['username', 'IP address', 'Port', 'login_time'])
        for row in list_users:
            user, ip, port, login_time = row
            user = QStandardItem(user)
            user.setEditable(False)
            ip = QStandardItem(ip)
            ip.setEditable(False)
            port = QStandardItem(str(port))
            port.setEditable(False)
            login_time = QStandardItem(str(login_time.replace(microsecond=0)))
            login_time.setEditable(False)
            user_list.appendRow([user, ip, port, login_time])
        self.active_clients_table.setModel(user_list)
        self.active_clients_table.resizeColumnsToContents()
        self.active_clients_table.resizeRowsToContents()

    # def show_statistics(self):
    #     global stat_window
    #     stat_window = StatWindow(self.database)
    #     stat_window.show()

    def server_config(self):
        """Method that creates a window with server settings."""

        global config_window
        config_window = ConfigWindow(self.config)
