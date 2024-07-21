import asyncio

import commands
from commands import Command, COMMANDS, CommandConverter
import utils

import logging

try:
    config = utils.read_json("../config.json")
except FileNotFoundError:
    config = utils.read_json("config.json")

HOST = config["GCS_IP"]
PORT = config["PORT"]
MSG_SIZE = config["MSG_SIZE"]


class TCPClient:
    def __init__(self, uav) -> None:
        self.uav = uav
        self.msg_queue: list[bytes] = [
            Command(type=COMMANDS.CONNECT, data={"successful": False}),
            Command(COMMANDS.MOVE_TO, data={}),
            Command(COMMANDS.TEST_RANGE_UBIQUITI, data={}),
        ]
        self.cmd_converter = CommandConverter()
        self.cmd2func = {
            COMMANDS.TEST_RANGE_UBIQUITI: self.uav.ubi_range_test()
        }  # to be changed by uav_comm.py

        self.logger = logging.Logger("TCPClient", logging.DEBUG)
        self.log_fh = logging.FileHandler("tcpclient.log")  # filehandle
        self.log_fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.log_fh)

    def add_cmd(self, cmd: commands.Command):
        msg = cmd
        self.msg_queue.append(msg)

    async def main(self):
        reader, writer = await asyncio.open_connection(HOST, PORT)
        # Initial Connection
        cmd = self.msg_queue.pop(0)
        encrypted = self.cmd_converter.msg_from_command(cmd)
        print(f"Sending: {cmd!r}")
        writer.write(encrypted)
        await writer.drain()

        incoming_data = await reader.read(MSG_SIZE)
        incoming_cmd = self.cmd_converter.command_from_msg(incoming_data)

        if incoming_cmd.type == COMMANDS.CONNECT:
            if incoming_cmd.data["successful"]:
                print("Communication with server has been established")
        print(incoming_cmd)

        while True:
            if len(self.msg_queue):
                cmd = self.msg_queue.pop(0)
                encrypted = self.cmd_converter.msg_from_command(cmd)
                writer.write(encrypted)
                await writer.drain()
            else:
                cmd = Command(COMMANDS.HEARTBEAT, {})
                encrypted = self.cmd_converter.msg_from_command(cmd)
                writer.write(encrypted)
                await writer.drain()

            # Read the response from the server
            incoming_data = await reader.read(MSG_SIZE)

            succesful = None
            try:
                incoming_cmd = self.cmd_converter.command_from_msg(incoming_data)
                succesful = True
            except Exception as e:
                self.logger.log(logging.DEBUG, e)
                succesful = False

            if not succesful:
                continue

            if cmd.type in self.cmd2func.keys():
                func_to_exec = self.cmd2func[cmd.type]
                func_to_exec(cmd.data)
            if cmd.type == COMMANDS.DISCONNECT:
                break
        print("closing the connection from client side")
        writer.close()
        await writer.wait_closed()

    def run(self):
        asyncio.run(self.main())


if __name__ == "__main__":
    tcp = TCPClient()
    tcp.run()
