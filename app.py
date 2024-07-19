import os
import sys

from utils import read_config

from ui.ui import UI

from process.video import VideoProcess

from threading import Event, Lock, Thread

from process.process import Process

CONFIG = read_config("ui/config.json")

global MEMORY
MEMORY = {"i": 0, "tiles_to_fetch": [], "videoStream":None}
global EVENTS
EVENTS = {"close_app": Event()}


class App:
    def __init__(self) -> None:
        self.ui = UI(CONFIG, MEMORY, EVENTS)
        self.process = Process(CONFIG)
        self.video_process = VideoProcess(CONFIG, MEMORY, self.ui.video_stream.screen_area)

    def run(self):
        try:
            self.process_thread = Thread(
                target=self.process.start, name="Process Thread", args=(MEMORY, EVENTS)
            )
            self.process_thread.start()
            self.video_thread = Thread(
                target=self.video_process.start, name="Video Stream Thread", args=()
            )
            self.video_thread.start()
            self.ui.start()
        except Exception as e:
            print("Error found:", e)
            EVENTS["close_app"].set()
            print("emitted close app event")
            self.process_thread.join(1)


if __name__ == "__main__":
    app = App()
    app.run()
