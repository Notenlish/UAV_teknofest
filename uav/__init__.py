import socket
import threading

from server.async_client import TCPClient
from streaming.server import start_ffmpeg_streaming, range_test_streaming

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
        self.comm_thread = threading.Thread(
            target=self._start_comm_thread, args=()
        )
        self.video_thread = threading.Thread(target=self._send_video, args=())

    def start_com_thread(self):
        print("ĞĞĞĞ CLİENT")
        try:
            self.comm_thread.start()
        except Exception as e:
            print(e)

    def start_vid_thread(self):
        self.video_thread.start()

    def start_ubi_thread(self, inc_data):  # this is called by TCPClient
        self._ubi_range_test()
        
    def _start_comm_thread(self):
        client = TCPClient(self)
        client.run()

    def _send_video(self):
        start_ffmpeg_streaming(GCS_IP, VIDEO_PORT, use_udp=VID_USE_UDP)

    def _ubi_range_test(self):
        def video_test():
            range_test_streaming(GCS_IP, UBI_RANGE_PORT, use_udp=VID_USE_UDP)

        self.video_thread = threading.Thread(target=video_test)
        self.video_thread.start()
