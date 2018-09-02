import logging

import os

from server.command.serverCommand import ServerCommand


class ServerDownloadCommand(ServerCommand):
    def __init__(self):
        self.__LOGGER = logging.getLogger(ServerDownloadCommand.__name__)

    def perform_command(self, param_string):
        self.__LOGGER.debug("Perform download command with args = " + str(param_string))
        if not os.path.exists("./" + str(param_string)):
            return None
        self.__LOGGER.debug("starting transmitting file = " + param_string)
        return param_string

    def is_exit_command(self):
        return False

    def is_upload_command(self):
        return False

    def is_download_command(self):
        return True
