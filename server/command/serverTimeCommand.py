import logging
from time import gmtime, strftime

from server.command.serverCommand import ServerCommand


class ServerTimeCommand(ServerCommand):
    def __init__(self):
        self.__LOGGER = logging.getLogger(ServerTimeCommand.__name__)

    def perform_command(self, param_string):
        self.__LOGGER.debug("performing time command with args = " + param_string)
        """
        getting current time in settled format (param_string)
        =====================================================
        :param param_string: time format
        :return: time in input format
        """
        return strftime(param_string, gmtime())

    def is_exit_command(self):
        return False

    def is_download_command(self):
        return False

    def is_upload_command(self):
        return False
