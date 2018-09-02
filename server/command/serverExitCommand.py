from server.command.serverCommand import ServerCommand


class ServerExitCommand(ServerCommand):
    def perform_command(self, param_string):
        return None

    def is_exit_command(self):
        return True
