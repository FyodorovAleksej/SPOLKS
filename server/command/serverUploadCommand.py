import logging
import os.path

from server.command.serverCommand import ServerCommand

FILE_POSTFIX = "1"


class ServerUploadCommand(ServerCommand):
    def __init__(self):
        self.__LOGGER = logging.getLogger(ServerUploadCommand.__name__)

    def perform_command(self, param_string):
        self.__LOGGER.debug("Perform upload command with args = " + str(param_string))
        while os.path.exists(str(param_string)):
            file_parts = str(param_string).rsplit(".", 1)
            extension = None
            if len(file_parts) == 2:
                extension = file_parts[1]
            name = None
            if len(file_parts) >= 1:
                name = file_parts[0]
            name += FILE_POSTFIX
            param_string = name + "." + extension
        self.__LOGGER.debug("receive file to = " + param_string)
        return param_string

    def is_exit_command(self):
        return False

    def is_upload_command(self):
        return True

    def is_download_command(self):
        return False
