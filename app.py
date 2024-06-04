import sys
import os

from utils import read_config

from ui.ui import UI
from process.process import Process

from threading import Thread, Event, Lock

CONFIG = read_config("ui/config.json")

global MEMORY
MEMORY = {"i": 0}
global EVENTS
EVENTS = {"close_app": Event()}


class App:
    def __init__(self) -> None:
        self.ui = UI(CONFIG)
        self.process = Process(CONFIG)

    def run(self):
        self.process_thread = Thread(
            target=self.process.start, name="Process Thread", args=(MEMORY, EVENTS)
        )
        self.process_thread.start()
        self.ui.start(MEMORY, EVENTS)
        self.process_thread.join()


if __name__ == "__main__":
    app = App()
    app.run()
