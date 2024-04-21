import asyncio

import utils
from commands import COMMANDS, Command, CommandConverter

config = utils.read_json("../config.json")

HOST = config["HOST"]
PORT = config["PORT"]
MSG_SIZE = config["MSG_SIZE"]


class TCPServer:
    def __init__(self) -> None:
        self.cmd_converter = CommandConverter()
        self.msg_queue: list[bytes] = []
    
    def add_command(self, cmd: Command):
        msg = self.cmd_converter.msg_from_command(cmd)
        self.msg_queue.append(msg)
    
    def remove_command(self, cmd: Command):
        msg = self.cmd_converter.msg_from_command(cmd)
        self.msg_queue.remove(msg)
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        incoming_data = await reader.read(MSG_SIZE)
        incoming_cmd = self.cmd_converter.command_from_msg(incoming_data)
        print(f"Received: {incoming_cmd}")
        if incoming_cmd.type == COMMANDS.CONNECT:
            new_cmd = Command(type=COMMANDS.CONNECT, data={"successful":True})
            response_msg = self.cmd_converter.msg_from_command(new_cmd)
            addr = writer.get_extra_info('peername')
            writer.write(response_msg)
            await writer.drain()
        
        while True:
            incoming_data = await reader.read(MSG_SIZE)
            incoming_cmd = self.cmd_converter.command_from_msg(incoming_data)
            if incoming_cmd.type == COMMANDS.NOTHING:
                if len(self.msg_queue):
                    msg_to_send = self.msg_queue.pop(0)
                    writer.write(msg_to_send)
                    await writer.drain()
            if incoming_cmd.type in Command2Function.cmd2func:
                Command2Function.cmd2func(incoming_cmd.type)(incoming_cmd.data) # run func associated
            if incoming_cmd.type == COMMANDS.DISCONNECT:
                print(f"closing connection to {addr}")
                writer.close()

    async def main(self):
        server = await asyncio.start_server(self.handle_client, HOST, PORT)
        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')
        
        async with server:
            await server.serve_forever()
    
    def run(self):
        asyncio.run(self.main())


if __name__ == "__main__":
    server = TCPServer()
    server.run()