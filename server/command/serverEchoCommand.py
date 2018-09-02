import logging
import re

from server.command.serverCommand import ServerCommand

ESCAPE_PART = "(\".*?\")|(\'.*?\')"


# echo command (echo "...")
# OPTIONS
# [-n] - echo string without go to new line
class ServerEchoCommand(ServerCommand):
    def __init__(self):
        self.__LOGGER = logging.getLogger(ServerEchoCommand.__name__)
        # bits of different flags
        self.__flags = {"-n": 2 ** 0}
        # current mode
        self.__mode = 0
        # mapping command mode to methods
        self.__mapping = {0: self.perform_mode_0, 1: self.perform_mode_1}

    def perform_command(self, param_string):
        self.__LOGGER.debug("performing echo command with args = " + param_string)
        """
        performing echo command
        :param param_string: params of command
        :return: result of performing echo command
        """
        # remove string like ["..." or '...'] from params
        clear_string = re.sub(ESCAPE_PART, "", param_string)
        # find flags
        for flag in self.__flags.keys():
            if flag in clear_string:
                # setting current mode with bit of found flag
                self.__mode = self.__mode | self.__flags[flag]
                # remove flag from raw params
                param_string = re.sub(flag, "", param_string)

        return self.__mapping[self.__mode](param_string)

    def is_exit_command(self):
        return False

    def is_download_command(self):
        return False

    def is_upload_command(self):
        return False

    def perform_mode_0(self, param_string):
        """
        performing command without any flag (mode = 0b00000000)
        =======================================================
        :param param_string: param of command
        :return: param string with endLine
        """
        return param_string + "\n"

    def perform_mode_1(self, param_string):
        """
        performing command with flag [-n] (mode = 0b00000001)
        =====================================================
        :param param_string: param of command
        :return: param string without endLine
        """
        return param_string
