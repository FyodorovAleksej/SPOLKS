import re

from server.command.serverDownloadCommand import ServerDownloadCommand
from server.command.serverEchoCommand import ServerEchoCommand
from server.command.serverExitCommand import ServerExitCommand
from server.command.serverTimeCommand import ServerTimeCommand
from server.command.serverUploadCommand import ServerUploadCommand

LINE_END = "\n|\r\n"
COMMAND_SEPARATOR = " "


# Parse receive text
class ServerParser:
    def __init__(self, socket):
        self.__commands = {"ECHO": ServerEchoCommand(),
                           "TIME": ServerTimeCommand(),
                           "EXIT": ServerExitCommand(),
                           "QUIT": ServerExitCommand(),
                           "CLOSE": ServerExitCommand(),
                           "DOWNLOAD": ServerDownloadCommand(),
                           "UPLOAD": ServerUploadCommand()}
        self.__socket = socket

    def parse_command(self, line):
        """
        parse receive line
        ==================
        :param line: line of received text
        :return: result of performing founded command
        """
        # split line to command and args
        command_parts = re.split(COMMAND_SEPARATOR, line, 1)
        print(command_parts)  # debug
        # getting command from diction
        params = None
        if len(command_parts) == 2:
            params = command_parts[1]
        command = None
        if command_parts[0].upper() in self.__commands.keys():
            command = self.__commands[command_parts[0].upper()]
        return command, params


def split_lines(input_text):
    """
    split text to lines by REG_EXP
    ==============================
    :param input_text: text to split
    :return: list of lines
    """
    return re.split(LINE_END, input_text)
