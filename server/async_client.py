import asyncio

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uav import UAVSoftware


try:
    from commands import Command, COMMANDS, CommandConverter
except ModuleNotFoundError:
    from server.commands import Command, COMMANDS, CommandConverter
import utils

import logging
import time

try:
    config = utils.read_config("../config.json")
except FileNotFoundError:
    config = utils.read_config("config.json")

HOST = config["GCS_IP"]
PORT = config["PORT"]
MSG_SIZE = config["MSG_SIZE"]


# UAV
class TCPClient:
    def __init__(self, uav: "UAVSoftware") -> None:
        self.uav = uav
        self.msg_queue: list[bytes] = [
            Command(type=COMMANDS.CONNECT, data={"successful": False}),
            Command(COMMANDS.MOVE_TO, data={}),
        ]
        self.cmd_converter = CommandConverter()
        self.cmd2func = {
            COMMANDS.TEST_RANGE_UBIQUITI: self.uav.start_ubi_thread
        }  # to be changed by uav_comm.py

        self.logger = logging.Logger("TCPClient", logging.DEBUG)
        self.log_fh = logging.FileHandler("tcpclient.log")  # filehandle
        self.log_fh.setLevel(logging.DEBUG)
        self.logger.addHandler(self.log_fh)

        self.time_since_heartbeat = 0
        self.start_time = time.time()

        print("ĞĞĞĞĞĞĞĞĞĞĞ async client")

    def add_cmd(self, cmd: Command):
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

        self.start_time = time.time()

        while True:  # write & read
            # print("32 async client")
            self.time_since_heartbeat = time.time() - self.start_time
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

            if self.time_since_heartbeat > 5:
                self.logger.log(
                    logging.DEBUG,
                    "OH NO! I CANT GET HEARTBEAT! I should just make it return to the starting point but its 1.04 AM and im not looking forward to working with this mess.",
                )

            if not succesful:
                continue
            # print(incoming_cmd)
            if incoming_cmd.type == COMMANDS.HEARTBEAT:
                self.time_since_heartbeat = 0
                self.start_time = time.time()
                # self.logger.log(logging.DEBUG, "HEARTBEAT")

            if incoming_cmd.type in self.cmd2func.keys():
                func = self.cmd2func[incoming_cmd.type]
                func(incoming_cmd.data)
            if incoming_cmd.type == COMMANDS.DISCONNECT:
                break
        print("closing the connection from client side")
        writer.close()
        await writer.wait_closed()

    def run(self):
        asyncio.run(self.main())


if __name__ == "__main__":
    tcp = TCPClient()
    tcp.run()
