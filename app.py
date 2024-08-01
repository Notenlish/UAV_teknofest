import logging
from threading import Event, Thread
import time

from process.gcs import GCSComm
from process.tile_proc import TileFetchProcess
from process.video import VideoProcess
from process.mav_comm import MavComm

from server.commands import COMMANDS, Command

from ui.ui import UI
from utils import read_config

CONFIG = read_config("config.json")

global MEMORY
MEMORY = {"tiles_to_fetch": [], "videoStream": None}
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
        self.mav_comm_process = MavComm(self, CONFIG, MEMORY)

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
            self.mav_thread = Thread(
                target=self.mav_comm_process.start, name="MAV Comm", args=()
            )
            self.mav_thread.start()
            self.ui.start()
        except Exception as e:
            print("Error found:", e)
            print("threads may be broken but the app is going strong!")
            # EVENTS["close_app"].set()
            # print("emitted close app event")
            # self.process_thread.join(1)

    def ubi_range_test(self):
        print("UBI RANGE TEST")
        self.comm_process.server.add_command(Command(COMMANDS.TEST_RANGE_UBIQUITI, {}))
        self.ubi_logger = logging.Logger("UBI LOG")
        self.ubi_fh = logging.FileHandler("ubi.log")
        self.ubi_logger.addHandler(self.ubi_fh)

        def a():
            import socket

            import numpy as np

            from utils import read_config

            try:
                config = read_config("../config.json")
            except FileNotFoundError:
                config = read_config("config.json")

            SEED = config["RANGE_TEST_SEED"]
            MSG_SIZE = config["MSG_SIZE"]
            GCS_IP = config["GCS_IP"]
            UBI_RANGE_PORT = config["UBI_RANGE_PORT"]

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                addr = (GCS_IP, UBI_RANGE_PORT)
                print("UBI ", addr)
                server_socket.bind(addr)
                server_socket.listen()
                print(f"UBI TEST Server listening on {addr}")

                while True:
                    client_socket, client_address = server_socket.accept()
                    start = time.time()
                    msg_freq = 20
                    msg_period = 1 / msg_freq
                    with client_socket:
                        while True:
                            # Receive data
                            incoming = client_socket.recv(MSG_SIZE)
                            # print(f"Received data {incoming[:10]}...")
                            incoming_buf = np.frombuffer(incoming, dtype=np.uint8)

                            np.random.seed(SEED)
                            u8_max = 2**8
                            orig_buf = np.array(
                                [
                                    round(np.random.random() * u8_max)
                                    for _ in range(MSG_SIZE)
                                ],
                                dtype=np.uint8,
                            )

                            correct_size = len(incoming_buf) == MSG_SIZE
                            if correct_size:
                                mismatched_elements = np.sum(orig_buf != incoming_buf)
                                # Calculate the corruption score
                                corruption_score = mismatched_elements / MSG_SIZE

                                # compare the data & received bytes
                                self.ubi_logger.log(
                                    logging.DEBUG,
                                    {
                                        "mismatch_num_count": mismatched_elements,
                                        "corruption": corruption_score,
                                        "time": time.time(),
                                    },
                                )

                            # Send the data
                            since_msg = time.time() - start
                            if since_msg < msg_period:
                                time.sleep(msg_period - since_msg)
                            start = time.time()
                            client_socket.sendall(orig_buf)

        self.video_thread = Thread(target=a, args=())
        self.video_thread.start()

    def start_vid(self):
        self.comm_process.server.add_command(Command(COMMANDS.START_VIDEO_STREAM, {}))

    def stop_vid(self):
        self.comm_process.server.add_command(Command(COMMANDS.STOP_VIDEO_STREAM, {}))


if __name__ == "__main__":
    try:

        class MPState:
            pass

        mpstate = MPState()
        mpstate.click_location = None  # get rid of err

        a = App(mpstate)
        a.run()
    except KeyboardInterrupt:
        EVENTS["close_app"].set()
        print("deleting app")
        del a.comm_process
        del a.comm_thread
        del a.video_process
        del a.video_thread
        del a
        print("AAAAAAAAAAAAAA KAFAYI YICEM TERMINAL KAPANMIYOR")
