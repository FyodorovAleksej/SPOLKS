import re

from server.command.serverEchoCommand import ServerEchoCommand
from server.command.serverExitCommand import ServerExitCommand
from server.command.serverTimeCommand import ServerTimeCommand

LINE_END = "\n|\r\n"
COMMAND_SEPARATOR = " "


# Parse receive text
class ServerParser:
    def __init__(self, socket):
        self.__commands = {"ECHO": ServerEchoCommand(),
                           "TIME": ServerTimeCommand(),
                           "EXIT": ServerExitCommand(),
                           "QUIT": ServerExitCommand(),
                           "CLOSE": ServerExitCommand()}
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
        command = self.__commands[command_parts[0].upper()]
        if command is not None:
            if command.is_exit_command():
                self.__socket.close()
                return None
            else:
                return command.perform_command(command_parts[1])
        else:
            return "Command not found \"" + line + "\""


def split_lines(input_text):
    """
    split text to lines by REG_EXP
    ==============================
    :param input_text: text to split
    :return: list of lines
    """
    return re.split(LINE_END, input_text)
