import configparser
import os
import sys

from PyQt5.QtWidgets import QApplication

from common.parser import Parser
from server.core import Server
from server.database import Storage
from server.server_gui import MainWindow


def main():
    """Server start function"""

    config = configparser.ConfigParser()
    dir_path = os.getcwd()
    config.read(f"{dir_path}/{'server.ini'}")

    connection = Parser()
    connection.arg_parser()
    ip_address = connection.ip_address
    port = connection.port
    database = Storage()
    server = Server(ip_address, port, database)
    server.daemon = True
    server.start()

    server_app = QApplication(sys.argv)
    main_window = MainWindow(database, config)
    server_app.exec_()


if __name__ == '__main__':
    main()
