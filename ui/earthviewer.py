import math
import os

import pygame
import requests
from dotenv import load_dotenv

load_dotenv()

# Tiles are available on zoom levels 0 through 22.
# style z=zoom x y[optionally the scale modifier] scale file_format api_key
URL = "https://tile.thunderforest.com/{}/{}/{}/{}.{}?apikey={}"


class EarthViewer:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area
        self.earth_move_speed = config["earthMoveSpeed"]

        self.zoom = 0
        self.max_tile_nums = (2**self.zoom) - 1
        self.scale = 2

        self.x = 0
        self.y = 0

    def move(self, x, y, dt):
        self.x += x * self.earth_move_speed * dt
        self.y += y * self.earth_move_speed * dt

    def change_zoom(self, amount):
        self.zoom += amount
        self.zoom = min(max(self.zoom, 0), 22)

    def set_scale(self, new_scale):
        self.scale = new_scale
        assert self.scale <= 2 and self.scale >= 1

    def _download_tile(
        self,
        zoom,
        x,
        y,
        style="landscape",
        file_format="png",
        cache_dir="ui/tiles",
    ):
        api_key = os.environ["THUNDERFOREST_API_KEY"]
        _y_str = f"{y}@{self.scale}x" if self.scale != 1 else y

        url = URL.format(style, zoom, x, _y_str, file_format, api_key)
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{self.scale}x.{file_format}"
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
        file_format="png",
        cache_dir="ui/tiles",
    ):
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{self.scale}x.{file_format}"
        )

        if not os.path.exists(tile_path):
            tile_path = self._download_tile(zoom, x, y)

        return tile_path

    def load_tile(self, zoom, x, y, cache_dir="ui/tiles"):
        tile_path = self._get_tile(zoom, x, y, cache_dir)
        return pygame.image.load(tile_path)

    def calculate_tiles(self):
        tile_w = 256 * self.scale
        tile_h = 256 * self.scale
        max_x = self.zoom**2 if self.zoom > 0 else 1
        max_y = max_x
        tiles = []
        for tile_x in range(math.ceil(self.screen_area.w / tile_w)):
            for tile_y in range(math.ceil(self.screen_area.h / tile_h)):
                normalized_x = tile_x % max_x
                normalized_y = tile_x % max_y
                tiles.append(
                    {
                        "normalized_x": normalized_x,
                        "normalized_y": normalized_y,
                        "screen_x": tile_x * tile_w + self.x,
                        "screen_y": tile_y * tile_h + self.y,
                    }
                )
        return tiles

    def render(self, screen: pygame.Surface):
        for tile in self.calculate_tiles():
            img = self.load_tile(self.zoom, tile["normalized_x"], tile["normalized_y"])
            rect = img.get_rect()
            screen.blit(img, (tile["screen_x"], tile["screen_y"]))


if __name__ == "__main__":
    pass
