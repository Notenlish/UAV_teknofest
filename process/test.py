import time
from threading import Event
import os
import pygame
import requests
from dotenv import load_dotenv

load_dotenv()

# Tiles are available on zoom levels 0 through 22.
# style z=zoom x y[optionally the scale modifier] scale file_format api_key
URL = "https://tile.thunderforest.com/{}/{}/{}/{}.{}?apikey={}"


class Process:
    def __init__(self, config: dict[str, any]) -> None:
        pass

    def start(self, MEMORY: dict[str, any], EVENTS: dict[str, Event]):
        while True:
            tiles_to_fetch: list = MEMORY["tiles_to_fetch"]
            if len(tiles_to_fetch) > 0:
                print(f"Tiles to fetch: {len(tiles_to_fetch)}")
                tile_info = tiles_to_fetch[0]
                result = self._download_tile(**tile_info)
                if result:
                    print(f"Successfully downloaded tile: {tile_info}")
                    tiles_to_fetch.pop(0)  # Ensure to remove the correct tile
                else:
                    print(f"Failed to download tile: {tile_info}")
                time.sleep(1)  # Add delay to prevent rate limiting issues
            MEMORY["i"] += 1
            if EVENTS["close_app"].is_set():
                break

    def _download_tile(
        self,
        scale,
        zoom,
        x,
        y,
        style="landscape",
        file_format="png",
        cache_dir="ui/tiles",
    ):
        print("Attempting to download file")
        api_key = os.environ["THUNDERFOREST_API_KEY"]
        _y_str = f"{y}@{scale}x" if scale != 1 else y

        url = URL.format(style, zoom, x, _y_str, file_format, api_key)
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{scale}x.{file_format}"
        )

        result = False
        if not os.path.exists(tile_path):
            print(f"Tile does not exist, attempting to get it from API: {url}")
            os.makedirs(cache_dir, exist_ok=True)
            response = requests.get(url)
            print(f"Response status code: {response.status_code}")
            if response.ok:
                with open(tile_path, "wb") as file:
                    file.write(response.content)
                result = True
            else:
                print("ERROR!", response.content)
        else:
            print("Tile already exists, skipping download")
        return result


if __name__ == "__main__":
    # Example usage
    MEMORY = {
        "tiles_to_fetch": [
            {"scale": 1, "zoom": 10, "x": 0, "y": 0},
            {"scale": 1, "zoom": 10, "x": 1, "y": 0},
            {"scale": 1, "zoom": 10, "x": 2, "y": 0},
            # Add more tiles as needed
        ],
        "i": 0,
    }
    EVENTS = {"close_app": Event()}

    process = Process(config={})
    process.start(MEMORY, EVENTS)
