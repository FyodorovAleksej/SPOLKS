import logging

from server.command.serverCommand import ServerCommand


class ServerExitCommand(ServerCommand):
    def __init__(self):
        self.__LOGGER = logging.getLogger(ServerExitCommand.__name__)

    def perform_command(self, param_string):
        self.__LOGGER.debug("Perform exit command with args = " + str(param_string))
        return None

    def is_exit_command(self):
        return True

    def is_upload_command(self):
        return False

    def is_download_command(self):
        return False
