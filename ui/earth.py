import requests
import os

import pygame

from dotenv import load_dotenv

load_dotenv()

# Tiles are available on zoom levels 0 through 22.
# style z=zoom x y[optionally the scale modifier as well] scale file_format api_key
URL = "https://tile.thunderforest.com/{}/{}/{}/{}.{}?apikey={}"


class EarthViewer:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area
        self.earth_move_speed = config["earthMoveSpeed"]
        try:
            self.earth = pygame.image.load("ui/earth.jpg").convert()
        except:
            print(
                "you don't have earth.jpg, please download it from https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74518/world.topo.200412.3x21600x10800.jpg"
            )

        self.zoom_steps = config["earthZoomSteps"]
        self.test_teams = config["testTeams"]

    def _download_tile(
        self,
        zoom,
        x,
        y,
        style="landscape",
        scale=1,
        file_format="png",
        cache_dir="ui/tiles",
    ):
        api_key = os.environ["THUNDERFOREST_API_KEY"]
        assert scale <= 2 and scale >= 1
        _y_str = f"{y}@{scale}x" if scale != 1 else y

        url = URL.format(style, zoom, x, _y_str, file_format, api_key)
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{scale}x.{file_format}"
        )

        if not os.path.exists(tile_path):
            os.makedirs(cache_dir, exist_ok=True)
            response = requests.get(url)
            if response.ok:
                with open(tile_path, "wb") as file:
                    file.write(response.content)
            else:
                print("ERROR!", str(response.content))

        return tile_path

    def _get_tile(
        self,
        zoom,
        x,
        y,
        style="landscape",
        scale=2,
        file_format="png",
        cache_dir="ui/tiles",
    ):
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{scale}x.{file_format}"
        )

        if not os.path.exists(tile_path):
            tile_path = self.download_tile(zoom, x, y, scale=scale)

        return tile_path

    def load_tile(self, zoom, x, y, cache_dir="ui/tiles"):
        tile_path = self.get_tile(zoom, x, y, cache_dir)
        return pygame.image.load(tile_path)


if __name__ == "__main__":
    pass
