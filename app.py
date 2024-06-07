import os
import sys

from utils import read_config

# couldnt figure out how to set project launch json, so this is how I will be able to launch app.py from ui.py

from ui.ui import UI

from threading import Event, Lock, Thread

from process.process import Process

CONFIG = read_config("ui/config.json")

global MEMORY
MEMORY = {"i": 0}
global EVENTS
EVENTS = {"close_app": Event()}


class App:
    def __init__(self) -> None:
        self.ui = UI(CONFIG, MEMORY, EVENTS)
        self.process = Process(CONFIG)

    def run(self):
        try:
            self.process_thread = Thread(
                target=self.process.start, name="Process Thread", args=(MEMORY, EVENTS)
            )
            self.process_thread.start()
            self.ui.start()
        except Exception as e:
            print(e)
            EVENTS["close_app"].set()
            print("emitted close app event")
            self.process_thread.join(1)


if __name__ == "__main__":
    app = App()
    app.run()
