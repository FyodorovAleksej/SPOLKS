from command import Command


class ExitCommand(Command):
    def perform_command(self, param_string):
        return None

    def is_exit_command(self):
        return True
