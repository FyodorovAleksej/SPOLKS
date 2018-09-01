#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from configobj import ConfigObj

from clientConnector import ClientConnector
from clientGui import Ui_Dialog

PROPERTIES_FILE = "./resources/clientconfig.ini"

CLIENT_PORT_KEY = "default_port"
CLIENT_SIZE_KEY = "default_size"
CLIENT_HOST_KEY = "client_server_host"
DISABLE_COLOR_KEY = "disable_color"
ENABLE_COLOR_KEY = "enable_color"

config = ConfigObj(PROPERTIES_FILE)

DEFAULT_PORT = int(config[CLIENT_PORT_KEY])
DEFAULT_HOST = config[CLIENT_HOST_KEY]
DEFAULT_SIZE = int(config[CLIENT_SIZE_KEY])

DISCONNECT_COLOR = config[DISABLE_COLOR_KEY]
CONNECT_COLOR = config[ENABLE_COLOR_KEY]


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        self.__client_connection = ClientConnector(DEFAULT_PORT, DEFAULT_HOST, DEFAULT_SIZE)
        self.__upload_path = None
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.portSpinBox.setValue(int(DEFAULT_PORT))
        self.ui.connectButton.setStyleSheet(DISCONNECT_COLOR)
        # SETTING signals
        self.ui.connectButton.clicked.connect(self.connect_slot)
        self.ui.disconnectButton.clicked.connect(self.disconnect_slot)
        self.ui.downloadButton.clicked.connect(self.download_slot)
        self.ui.sendButton.clicked.connect(self.send_slot)
        self.ui.uploadButton.clicked.connect(self.upload_slot)
        self.ui.uploadToolButton.clicked.connect(self.upload_browse_slot)

        # self.ui.ejectButton.clicked.connect(self.eject)

    # close action
    def close_event(self, event):
        self.__client_connection.close()
        event.accept()

    def log_info(self, message):
        if message is not None:
            self.ui.infoLabel.setText("info: " + message)

    def connect_slot(self):
        self.__client_connection.set_port(self.ui.portSpinBox.value())
        if self.__client_connection.connect():
            self.ui.connectButton.setStyleSheet(CONNECT_COLOR)

    def disconnect_slot(self):
        if self.__client_connection.close():
            self.ui.connectButton.setStyleSheet(DISCONNECT_COLOR)

    def send_slot(self):
        if self.__client_connection.send(self.ui.inputTextArea.toPlainText().encode()):
            self.log_info("sending was completed")
            self.log_info("receive = " + self.__client_connection.receive())
        else:
            self.log_info("sending wasn't complete")

    def upload_browse_slot(self):
        self.__upload_path = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)")[0]
        self.ui.uploadFileLineEdit.setText(self.__upload_path)

    def upload_slot(self):
        if self.__upload_path:
            pass
        else:
            self.log_info("path for file to upload wasn't setted")

    def download_slot(self):
        down_path = self.ui.downloadFileLineEdit.text()
        if down_path:
            pass
        else:
            self.log_info("download path wasn't setted")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()

    sys.exit(app.exec_())
exit()
