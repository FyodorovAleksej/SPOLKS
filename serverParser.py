import re

from echoCommand import EchoCommand
from exitCommand import ExitCommand
from timeCommand import TimeCommand

LINE_END = "\n|\r\n"
COMMAND_SEPARATOR = " "


class ServerParser:
    def __init__(self, socket):
        self.__commands = {"ECHO": EchoCommand(),
                           "TIME": TimeCommand(),
                           "EXIT": ExitCommand(),
                           "QUIT": ExitCommand(),
                           "CLOSE": ExitCommand()}
        self.__socket = socket

    def parse_command(self, line):
        command_parts = re.split(COMMAND_SEPARATOR, line, 1)
        print(command_parts)
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
    return re.split(LINE_END, input_text)
