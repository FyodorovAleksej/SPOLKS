#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from configobj import ConfigObj

import commonFileLib
from client.clientConnector import ClientConnector
from client.gui.clientGui import Ui_Dialog


# Logging settings
logging.basicConfig(handlers=[
        logging.FileHandler(u"clientLog.log"),
        logging.StreamHandler()
    ], format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG)


# Path to properties file
PROPERTIES_FILE = "./resources/clientconfig.ini"

# Keys for properties file
# Socket port for connect
CLIENT_PORT_KEY = "default_port"
# Max size of bytes per send
CLIENT_SIZE_KEY = "default_size"
# Host to connect
CLIENT_HOST_KEY = "client_server_host"
# Colors of connection button
DISABLE_COLOR_KEY = "disable_color"
ENABLE_COLOR_KEY = "enable_color"

# Reading by properties
config = ConfigObj(PROPERTIES_FILE)

DEFAULT_PORT = int(config[CLIENT_PORT_KEY])
DEFAULT_HOST = config[CLIENT_HOST_KEY]
DEFAULT_SIZE = int(config[CLIENT_SIZE_KEY])

DISCONNECT_COLOR = config[DISABLE_COLOR_KEY]
CONNECT_COLOR = config[ENABLE_COLOR_KEY]


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        """
        create window (PyQt5)
        =====================
        :param parent: parent window
        """
        self.__client_connection = ClientConnector(DEFAULT_PORT, DEFAULT_HOST, DEFAULT_SIZE)
        self.__upload_path = None
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Set window startup settings
        self.ui.portSpinBox.setValue(int(DEFAULT_PORT))
        self.ui.connectButton.setStyleSheet(DISCONNECT_COLOR)

        # Mapping signals to slots
        self.ui.connectButton.clicked.connect(self.connect_slot)
        self.ui.disconnectButton.clicked.connect(self.disconnect_slot)
        self.ui.downloadButton.clicked.connect(self.download_slot)
        self.ui.sendButton.clicked.connect(self.send_slot)
        self.ui.uploadButton.clicked.connect(self.upload_slot)
        self.ui.uploadToolButton.clicked.connect(self.upload_browse_slot)

    def close_event(self, event):
        """
        slot, that call on close window
        ===============================
        :param event: event of closing window
        :return: None - always
        """
        self.__client_connection.close()
        event.accept()

    def log_info(self, message):
        """
        method for logging message in logLabel in window
        ================================================
        :param message: message to logging
        :return: None - always
        """
        if message is not None:
            self.ui.infoLabel.setText("info: " + message)

    def connect_slot(self):
        """
        connect to settled host and port
        ================================
        :return: None - always
        """
        self.__client_connection.set_port(self.ui.portSpinBox.value())
        if self.__client_connection.connect() == 0:
            # Change color of <connect> button
            self.log_info("connect fail")
            self.ui.connectButton.setStyleSheet(DISCONNECT_COLOR)
        else:
            self.log_info("connected successfully")
            self.ui.connectButton.setStyleSheet(CONNECT_COLOR)

    def disconnect_slot(self):
        """
        disconnect from host and port
        =============================
        :return: None - always
        """
        if self.__client_connection.close() != 0:
            self.ui.connectButton.setStyleSheet(DISCONNECT_COLOR)

    def send_slot(self):
        """
        send text from textArea by socket to host
        =========================================
        :return: None - always
        """
        if self.__client_connection.send(self.ui.inputTextArea.toPlainText().encode()):
            self.log_info("sending was completed")
            self.log_info("receive = " + self.__client_connection.receive())
        else:
            self.log_info("sending wasn't complete")

    def upload_browse_slot(self):
        """
        choose file for upload (open fileDialog)
        ========================================
        :return: None - always
        """
        self.__upload_path = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)")[0]
        self.ui.uploadFileLineEdit.setText(self.__upload_path)

    def upload_slot(self):
        """
        upload chosen file to server by socket
        ======================================
        :return: None - always
        """
        if self.__upload_path:
            self.__client_connection.send(("UPLOAD " + str(self.__upload_path) + "\n").encode())
            commonFileLib.send_file(self.__client_connection, self.__upload_path, DEFAULT_SIZE)
        else:
            self.log_info("path for file to upload wasn't settled")

    def download_slot(self):
        """
        download settled path from server to temp file
        :return: None - always
        """
        down_path = self.ui.downloadFileLineEdit.text()
        if down_path:
            self.__client_connection.send(("DOWNLOAD " + str(down_path) + "\n").encode())
            commonFileLib.receive_file(self.__client_connection, self.__upload_path, "")
        else:
            self.log_info("download path wasn't setted")


# Main
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()

    sys.exit(app.exec_())
exit()
