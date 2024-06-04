import time
from threading import Event


class Process:
    def __init__(self, config: dict[str, any]) -> None:
        pass

    def start(self, MEMORY: dict[str, any], EVENTS: dict[str, Event]):
        while True:
            time.sleep(1)
            MEMORY["i"] += 1
            if EVENTS["close_app"].is_set():
                break
