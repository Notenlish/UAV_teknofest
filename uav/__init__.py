import socket
import threading

from server.async_server import TCPServer
from streaming.server import start_ffmpeg_streaming

from utils import read_config

try:
    CONFIG = read_config("../config.json")
except FileNotFoundError:
    CONFIG = read_config("config.json")

GCS_IP = CONFIG["GCS_IP"]
PORT = CONFIG["PORT"]


class UAVSoftware:
    def __init__(self) -> None:
        self.comm_thread = threading.Thread(target=self.start_comm_thread, args=(self,))
        self.video_thread = threading.Thread(target=self.send_video, args=(self,))

    def start_comm_thread(self):
        server = TCPServer()
        server.run()
    
    def send_video(self):
        start_ffmpeg_streaming()

    def ubi_range_test(self, inc_data: dict):
        self.video_thread = 
        pass
