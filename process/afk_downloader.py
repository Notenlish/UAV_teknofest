from threading import Event, Lock, Thread

from process import Process

import time

import os

CONFIG = {}

global MEMORY
MEMORY = {"i": 0, "tiles_to_fetch": []}
global EVENTS
EVENTS = {"close_app": Event()}


class Downloader:
    def __init__(self, memory) -> None:
        self.zoom = 0
        self._calculate_max_tiles()

        self.scale = 1
        self.style = "landscape"
        self.file_format = "png"
        self.cache_dir = "ui/tiles"

        self.memory = memory

    def _calculate_max_tiles(self):
        self.max_tile_nums = 2**self.zoom if self.zoom != 0 else 1

    def set_zoom(self, new_amount):
        self.zoom = new_amount
        self.zoom = min(max(self.zoom, 0), 22)
        self._calculate_max_tiles()

    def set_scale(self, new_scale):
        self.scale = new_scale
        assert self.scale <= 2 and self.scale >= 1

    def calculate_tiles(self):
        start_x = 0
        start_y = 0

        end_x = self.max_tile_nums
        end_y = self.max_tile_nums

        tile_id = 0
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if self.zoom == 0:
                    tile_id = 0

                max_tile_x = self.max_tile_nums
                max_tile_y = max_tile_x

                tile_x = tile_id % max_tile_x
                tile_y = (tile_id // max_tile_y) % max_tile_y
                tile_path = f"{self.style}_{self.zoom}_{tile_x}_{tile_y}_{self.scale}x.{self.file_format}"

                if os.path.exists(os.path.join(self.cache_dir, tile_path)):
                    continue
                else:  # file doesnt exist
                    tiles_to_fetch: list = self.memory["tiles_to_fetch"]
                    tile = {
                        "scale": self.scale,
                        "zoom": self.zoom,
                        "x": tile_x,
                        "y": tile_y,
                    }
                    try:
                        tiles_to_fetch.index(tile)
                    except ValueError:  # tile wasnt added to fetch list
                        tiles_to_fetch.append(tile)

                tile_id += 1

    def run(self, zoom):
        self.set_zoom(zoom)
        self.calculate_tiles()


class A:
    def __init__(self) -> None:
        self.process = Process(CONFIG)
        self.downloader = Downloader(MEMORY)

    def run(self):
        try:
            self.process_thread = Thread(
                target=self.process.start, name="Process Thread", args=(MEMORY, EVENTS)
            )
            self.process_thread.start()
            for zoom in range(22 + 1):
                self.downloader.run(zoom)
                while True:
                    time.sleep(0.1)
                    if len(MEMORY["tiles_to_fetch"]) == 0:
                        break
        except Exception as e:
            print("Error found:", e)
            EVENTS["close_app"].set()
            print("emitted close app event")
            self.process_thread.join(1)


if __name__ == "__main__":
    a = A()
    a.run()
