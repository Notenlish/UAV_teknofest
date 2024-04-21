import asyncio

import commands
import utils

config = utils.read_json("../config.json")

HOST = config["HOST"]
PORT = config["PORT"]
MSG_SIZE = config["MSG_SIZE"]


class TCPClient:
    def __init__(self) -> None:
        self.msg_queue: list[bytes] = []
        self.cmd_converter = commands.CommandConverter()
        self.add_cmd(
            commands.Command(type=commands.COMMANDS.CONNECT, data={"successful": False})
        )
        self.cmd2func = {}  # to be changed by uav_comm.py

    def add_cmd(self, cmd: commands.Command):
        msg = self.cmd_converter.msg_from_command(cmd)
        self.msg_queue.append(msg)

    async def main(self):
        reader, writer = await asyncio.open_connection(HOST, PORT)
        # Initial Connection
        message = self.msg_queue.pop(0)
        print(f"Sending: {message!r}")
        writer.write(message)
        await writer.drain()

        data = await reader.read(MSG_SIZE)
        incoming_cmd = self.cmd_converter.command_from_msg(data)
        print(incoming_cmd)
        if incoming_cmd.type == commands.COMMANDS.CONNECT:
            if incoming_cmd.data["successful"]:
                print("Communication with server has been established")

        while True:
            if len(self.msg_queue):
                message = self.msg_queue.pop(0)
                writer.write(message.encode())
                await writer.drain()
            # what to do if there's no message to send
            # Send a message to the server so it has the sending rights?
            # print(f'Sending: {message!r}')
            # writer.write(message.encode())
            # await writer.drain()

            # Read the response from the server
            data = await reader.read(MSG_SIZE)
            cmd = self.cmd_converter.command_from_msg(data)
            if cmd.type in self.cmd2func.keys():
                func_to_exec = self.cmd2func[cmd.type]
                func_to_exec(cmd.data)
            if cmd.type == commands.COMMANDS.DISCONNECT:
                break
        print("closing the connection from client side")
        writer.close()
        await writer.wait_closed()

    def run(self):
        asyncio.run(self.main())


if __name__ == "__main__":
    tcp = TCPClient()
    tcp.run()
