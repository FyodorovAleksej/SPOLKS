import re

from command import Command

ESCAPE_PART = "(\".*?\")|(\'.*?\')"


class EchoCommand(Command):
    def __init__(self):
        self.__flags = {"-n": 2 ** 0}
        self.__mode = 0
        self.__mapping = {0: self.perform_mode_0, 1: self.perform_mode_1}

    def perform_command(self, param_string):
        print("param_string = " + param_string)
        clear_string = re.sub(ESCAPE_PART, "", param_string)
        print("clear_string = " + clear_string)
        for flag in self.__flags.keys():
            if flag in clear_string:
                self.__mode = self.__mode | self.__flags[flag]
                param_string = re.sub(flag, "", param_string)

        return self.__mapping[self.__mode](param_string)

    def is_exit_command(self):
        return False

    def perform_mode_0(self, param_string):
        return param_string + "\n"

    def perform_mode_1(self, param_string):
        return param_string
