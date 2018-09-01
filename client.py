#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView, QFileDialog
from clientGui import Ui_Dialog
from clientConnector import ClientConnector

DEFAULT_PORT = 9080
DEFAULT_SIZE = 1024
DEFAULT_HOST = "localhost"

CONNECT_COLOR = QColor(155, 255, 155)
DISCONNECT_COLOR = QColor(255, 155, 155)


class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        self.__client_connection = ClientConnector(DEFAULT_PORT, DEFAULT_HOST, DEFAULT_SIZE)
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # SETTING signals
        self.ui.connectButton.clicked.connect(self.connectSlot)
        self.ui.disconnectButton.clicked.connect(self.disconnectSlot)
        self.ui.downloadButton.clicked.connect(self.downloadSlot)
        self.ui.sendButton.clicked.connect(self.sendSlot)
        self.ui.uploadButton.clicked.connect(self.uploadSlot)
        self.ui.uploadToolButton.clicked.connect(self.uploadBrowseSlot)

        # self.ui.ejectButton.clicked.connect(self.eject)

    # close action
    def closeEvent(self, event):
        self.__client_connection.close()
        event.accept()

    def logInfo(self, message):
        if (message != None):
            self.ui.infoLabel.setText("info: " + message)

    def connectSlot(self):
        self.__client_connection.set_port(self.ui.portSpinBox.value())
        if self.__client_connection.connect():
            self.ui.connectButton.setBackground(CONNECT_COLOR)

    def disconnectSlot(self):
        if self.__client_connection.close():
            self.ui.connectButton.setBackground(DISCONNECT_COLOR)

    def sendSlot(self):
        if self.__client_connection.send(self.ui.inputTextArea.toPlainText().encode()):
            self.logInfo("sending was completed")
            self.logInfo("receive = " + self.__client_connection.receive())
        else:
            self.logInfo("sending wasn't complete")

    def uploadBrowseSlot(self):
        self.__upload_path = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)")
        self.ui.uploadFileLineEdit.setText(self.__upload_path)

    def uploadSlot(self):
        if self.__upload_path:
            pass
        else:
            self.logInfo("path for file to upload wasn't setted")

    def downloadSlot(self):
        downPath = self.ui.downloadFileLineEdit.text()
        if downPath:
            pass
        else:
            self.logInfo("download path wasn't setted")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()

    sys.exit(app.exec_())
exit()