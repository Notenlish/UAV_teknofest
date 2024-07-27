import time
from threading import Event, Thread
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Tiles are available on zoom levels 0 through 22.
# style z=zoom x y[optionally the scale modifier] file_format api_key
URL = "https://{}.tile.thunderforest.com/{}/{}/{}/{}.{}?apikey={}"


class TileFetchProcess:
    def __init__(self, config: dict[str, any]) -> None:
        pass

    def fetch(self, MEMORY: dict[str, any], EVENTS: dict[str, Event], subdomain: str):
        while True:
            fetch_list: list = MEMORY["tiles_to_fetch"]
            if len(fetch_list) > 0:
                for tile in fetch_list:
                    if not tile["taken"]:
                        tile["taken"] = True
                        result = self._download_tile(**tile, subdomain=subdomain)
                        if result:
                            # print(f"Successfully downloaded tile: {tile}")
                            fetch_list.remove(tile)  # Ensure to remove the correct tile
                        else:
                            tile["taken"] = False
                            print(f"Failed to download tile: {tile}")
            time.sleep(0.5)
            if EVENTS["close_app"].is_set():
                break

    def start(self, MEMORY: dict[str, any], EVENTS: dict[str, Event]):
        threads = [
            Thread(target=self.fetch, name=f"{letter} fetcher", args=(MEMORY, EVENTS, letter))
            for letter in "abc"
        ]
        for t in threads:
            t.start()

    def _download_tile(
        self,
        scale,
        zoom,
        x,
        y,
        taken,
        subdomain,
        style="landscape",
        file_format="png",
        cache_dir="ui/tiles",
    ):
        # print("Attempting to download file")
        api_key = os.environ["THUNDERFOREST_API_KEY"]
        _y_str = f"{y}@{scale}x" if scale != 1 else y

        url = URL.format(subdomain, style, zoom, x, _y_str, file_format, api_key)
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{scale}x.{file_format}"
        )

        result = False
        if not os.path.exists(tile_path):
            # print(f"Tile does not exist, attempting to get it from API: {url}")
            os.makedirs(cache_dir, exist_ok=True)
            response = requests.get(url)
            # print(f"Response status code: {response.status_code}")
            if response.ok:
                with open(tile_path, "wb") as file:
                    file.write(response.content)
                result = True
            else:
                print("ERROR!", response.content)
        else:
            result = True
            # print("Tile already exists, skipping download")
        return result
