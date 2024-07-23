import socket
import threading

from server.async_client import TCPClient
from streaming.server import range_test_streaming
from streaming.video_thread import VideoThread

from utils import read_config

try:
    CONFIG = read_config("../config.json")
except FileNotFoundError:
    CONFIG = read_config("config.json")

GCS_IP = CONFIG["GCS_IP"]
PORT = CONFIG["PORT"]
VIDEO_PORT = CONFIG["VIDEO_PORT"]
RANGE_TEST_SEED = CONFIG["RANGE_TEST_SEED"]
VID_USE_UDP = CONFIG["VID_USE_UDP"]
UBI_RANGE_PORT = CONFIG["UBI_RANGE_PORT"]


class UAVSoftware:
    def __init__(self) -> None:
        self.vid_active = False
        self.comm_thread = threading.Thread(target=self._start_comm_thread, args=())

    def start_com_thread(self):
        print("ĞĞĞĞ CLİENT")
        try:
            self.comm_thread.start()
        except Exception as e:
            print(e)

    def start_vid(self, inc_data):
        self.video_thread = VideoThread("UAV Vid Thread", CONFIG)
        self.video_thread.run()
        
    def stop_vid(self, inc_data):
        self.video_thread.stop()

    def start_ubi_thread(self, inc_data):  # this is called by TCPClient
        self._ubi_range_test()

    def _start_comm_thread(self):
        client = TCPClient(self, CONFIG)
        client.run()

    def _ubi_range_test(self):
        def video_test():
            range_test_streaming(GCS_IP, UBI_RANGE_PORT, use_udp=VID_USE_UDP)

        self.video_thread = threading.Thread(target=video_test)
        self.video_thread.start()
