import math
import os

import pygame
import requests
from dotenv import load_dotenv

from utils import draw_text

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
            print("tile doesnt exist, attempting to get it from api")
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

        start_x = math.floor(0 / tile_w) - 1
        end_x = math.ceil((0 + self.screen_area.w) / tile_w)
        start_y = math.floor(0 / tile_h) - 1
        end_y = math.ceil((0 + self.screen_area.h) / tile_h)

        tile_id = 0
        tiles = []
        for x in range(start_x, end_x):
            offset_x = self.x % tile_w
            screen_x = x * tile_w + offset_x
            for y in range(start_y, end_y):
                offset_y = self.y % tile_h
                screen_y = y * tile_h + offset_y

                if self.zoom == 0:
                    tile_id = 0

                tile_rect = pygame.Rect(screen_x, screen_y, tile_w, tile_h)
                tile_rect = tile_rect.move(offset_x, offset_y)
                tile = {
                    "x": tile_rect.x,
                    "y": tile_rect.y,
                    "w": tile_rect.w,
                    "h": tile_rect.h,
                    "id": tile_id,
                }
                tiles.append(tile)
                tile_id += 1
            tile_id += 1
            return tiles

    def render(self, screen: pygame.Surface, font: pygame.Font):
        for tile in self.calculate_tiles():
            tile_rect = pygame.Rect(tile["x"], tile["y"], tile["w"], tile["h"])
            tile_id = tile["id"]

            max_tile_x = self.zoom**2 if self.zoom > 0 else 1
            max_tile_y = max_tile_x

            tile_x = tile_id // max_tile_x
            tile_y = tile_id % max_tile_x


            print("debug:", f"zoom:{self.zoom} id:{tile_id} tilex:{tile_x} tiley{tile_y} maxx{max_tile_x} maxy{max_tile_y}")
            img = self.load_tile(self.zoom, tile_x, tile_y)

            screen.blit(img, tile_rect.topleft)
            pygame.draw.rect(screen, "grey", tile_rect, 3)
            draw_text(screen, font, str(tile_id), tile_rect.center)


if __name__ == "__main__":
    pass
