import sys
import os

from utils import read_config


# couldnt figure out how to set project launch json, so this is how I will be able to launch app.py from ui.py
try:
    from ui.ui import UI
except ModuleNotFoundError:
    from ui import UI


from process.process import Process

from threading import Thread, Event, Lock

CONFIG = read_config("ui/config.json")

global MEMORY
MEMORY = {"i": 0, "earth_scaled": {}}
global EVENTS
EVENTS = {"close_app": Event()}


class App:
    def __init__(self) -> None:
        self.ui = UI(CONFIG)
        self.process = Process(CONFIG)

    def run(self):
        try:
            self.process_thread = Thread(
                target=self.process.start, name="Process Thread", args=(MEMORY, EVENTS)
            )
            self.process_thread.start()
            self.ui.start(MEMORY, EVENTS)
        except Exception as e:
            print(e)
            EVENTS["close_app"].set()
            print("emitted close app event")
            self.process_thread.join(1)


if __name__ == "__main__":
    app = App()
    app.run()
