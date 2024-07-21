import os
import sys

from utils import read_config

from ui.ui import UI

from threading import Event, Lock, Thread

from process.tile_proc import TileFetchProcess
from process.video import VideoProcess
from process.gcs import GCSComm

from server.commands import COMMANDS, Command

import logging

CONFIG = read_config("ui/config.json")

c1, c2 = read_config("config.json"), read_config("ui/config.json")
if c1["VIDEO_PORT"] != c2["videoPort"]:
    print("Zort! Video çalışmayacak çünkü portlar aynı değil.")
if c1["VID_USE_UDP"] != c2["sendVideoUDP"]:
    print("Zort! Video çalışmayacak çünkü UDP/TCP aynı değil.")

global MEMORY
MEMORY = {"i": 0, "tiles_to_fetch": [], "videoStream": None}
global EVENTS
EVENTS = {"close_app": Event()}


class App:
    def __init__(self, mpstate) -> None:
        self.mpstate = mpstate
        self.ui = UI(self, CONFIG, MEMORY, EVENTS)
        self.tile_process = TileFetchProcess(CONFIG)
        self.video_process = VideoProcess(
            CONFIG, MEMORY, self.ui.video_stream.screen_area
        )
        self.comm_process = GCSComm(self, CONFIG, MEMORY)

    def run(self):
        try:
            self.process_thread = Thread(
                target=self.tile_process.start,
                name="Process Thread",
                args=(MEMORY, EVENTS),
            )
            self.process_thread.start()
            self.video_thread = Thread(
                target=self.video_process.start, name="Video Stream Thread", args=()
            )
            self.video_thread.start()
            self.comm_thread = Thread(
                target=self.comm_process.start, name="GCS Comm", args=()
            )
            self.comm_thread.start()
            self.ui.start()
        except Exception as e:
            print("Error found:", e)
            EVENTS["close_app"].set()
            print("emitted close app event")
            self.process_thread.join(1)

    def ubi_range_test(self):
        print("UBI RANGE TEST")
        self.comm_process.server.add_command(Command(COMMANDS.TEST_RANGE_UBIQUITI, {}))
        self.ubi_logger = logging.Logger("UBI LOG")
        self.ubi_fh = logging.FileHandler("ubi.log")
        self.ubi_logger.addHandler(self.ubi_fh)

        def a():
            print("lmao")
            import socket
            import numpy as np
            from utils import read_config

            try:
                config = read_config("../config.json")
            except FileNotFoundError:
                config = read_config("config.json")

            SEED = config["RANGE_TEST_SEED"]
            MSG_SIZE = config["MSG_SIZE"]
            UAV_IP = config["UAV_IP"]
            UBI_RANGE_PORT = config["UBI_RANGE_PORT"]

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                addr = (UAV_IP, UBI_RANGE_PORT)
                server_socket.bind(addr)
                server_socket.listen()
                print(f"UBI TEST Server listening on {addr}")

                client_socket, client_address = server_socket.accept()
                while True:
                    # Receive data
                    incoming = client_socket.recv(MSG_SIZE)
                    # print(f"Received data {incoming[:10]}...")
                    incoming_buf = np.frombuffer(incoming, dtype=np.uint8)

                    np.random.seed(SEED)
                    u8_max = 2**8
                    orig_buf = np.array(
                        [round(np.random.random() * u8_max) for _ in range(MSG_SIZE)],
                        dtype=np.uint8,
                    )

                    # compare the data & received bytes
                    self.ubi_logger.log(
                        logging.DEBUG,
                        {"original": list(orig_buf), "arrived": list(incoming)},
                    )
                    # if orig_buf == incoming:
                    #     print("OHA AYNI VERI GELDI")
                    # else:
                    #     print("zorttiri zort zort")

                    # Send the data
                    client_socket.sendall(orig_buf)

        self.video_thread = Thread(target=a, args=())
        self.video_thread.run()


if __name__ == "__main__":

    class MPState:
        pass

    mpstate = MPState()
    mpstate.click_location = None  # get rid of err

    a = App(mpstate)
    a.run()
