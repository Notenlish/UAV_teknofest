from async_server import TCPServer
from commands import Command, CommandConverter


class GroundControlSystem:
    def __init__(self) -> None:
        self.tcp_server = TCPServer()

    def add_cmd_to_queue(self, cmd: Command):
        self.tcp_server.add_command(cmd)

    def remove_cmd_from_queue(self, cmd: Command):
        self.tcp_server.remove_command(cmd)
