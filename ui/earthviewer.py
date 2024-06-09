import math
import os

import pygame
import requests
from dotenv import load_dotenv

from utils import draw_text


class EarthViewer:
    def __init__(
        self, config: dict[str, any], memory: dict[str, any], screen_area: pygame.Rect
    ) -> None:
        self.screen_area = screen_area
        self.earth_move_speed = config["earthMoveSpeed"]
        self.memory = memory

        self.zoom = 0
        self._calculate_max_tiles()
        self.scale = 1

        self.camera_x = 0
        self.camera_y = 0

    def _calculate_max_tiles(self):
        self.max_tile_nums = 2**self.zoom if self.zoom != 0 else 1

    def move(self, x, y, dt):
        self.camera_x += x * self.earth_move_speed * dt
        self.camera_y += y * self.earth_move_speed * dt

    def change_zoom(self, amount):
        self.zoom += amount
        self.zoom = min(max(self.zoom, 0), 22)
        self._calculate_max_tiles()

    def set_scale(self, new_scale):
        self.scale = new_scale
        assert self.scale <= 2 and self.scale >= 1

    def _get_tile(
        self,
        zoom,
        x,
        y,
        style="landscape",
        file_format="png",
        cache_dir="ui/tiles",
    ):
        # print(f"style:{style} zoom:{zoom} x:{x} y:{y} scale:{self.scale}")
        tile_path = os.path.join(
            cache_dir, f"{style}_{zoom}_{x}_{y}_{self.scale}x.{file_format}"
        )

        if not os.path.exists(tile_path):
            tile_path = None
            tiles_to_fetch: list = self.memory["tiles_to_fetch"]
            tile = {"scale": self.scale, "zoom": zoom, "x": x, "y": y}
            try:
                tiles_to_fetch.index(tile)
            except ValueError:
                tiles_to_fetch.append(tile)

        return tile_path

    def load_tile(
        self, zoom, x, y, cache_dir="ui/tiles", style="landscape", file_format="png"
    ):
        tile_path = f"{style}_{zoom}_{x}_{y}_{self.scale}x.{file_format}"
        try:
            img = self.memory["tiles_loaded"][tile_path]
        except KeyError:
            tile_path = self._get_tile(zoom, x, y, cache_dir=cache_dir)
            if tile_path == None:
                if self.scale == 1:
                    return pygame.image.load("ui/data/empty.png")
                elif self.scale == 2:
                    return pygame.image.load("ui/data/empty@2x.png")
            img = pygame.image.load(tile_path)
            self.memory["tiles_loaded"][tile_path] = img
        return img

    def calculate_tiles(self, screen, font):
        tile_w = 256 * self.scale
        tile_h = 256 * self.scale

        start_x = 0
        start_y = 0

        end_x = self.max_tile_nums
        end_y = self.max_tile_nums

        tile_id = 0
        tiles = []
        for y in range(start_y, end_y):
            offset_y = self.camera_y  # % tile_h
            screen_y = y * tile_h + offset_y
            for x in range(start_x, end_x):
                offset_x = self.camera_x  # % tile_w
                screen_x = x * tile_w + offset_x

                if self.zoom == 0:
                    tile_id = 0

                tile_rect = pygame.Rect(screen_x, screen_y, tile_w, tile_h)

                tile = {
                    "x": tile_rect.x,
                    "y": tile_rect.y,
                    "w": tile_rect.w,
                    "h": tile_rect.h,
                    "id": tile_id,
                }
                tiles.append(tile)

                tile_id += 1
        return tiles

    def render(self, screen: pygame.Surface, font: pygame.Font):
        for tile in self.calculate_tiles(screen, font):
            tile_rect = pygame.Rect(tile["x"], tile["y"], tile["w"], tile["h"])
            tile_id = tile["id"]

            max_tile_x = self.max_tile_nums
            max_tile_y = max_tile_x

            tile_x = tile_id % max_tile_x
            tile_y = (tile_id // max_tile_y) % max_tile_y

            # print(
            #    f"id:{tile_id} x:{tile_x} y:{tile_y} maxX:{max_tile_x} maxY:{max_tile_y}"
            # )

            img = self.load_tile(self.zoom, tile_x, tile_y)

            screen.blit(img, tile_rect.topleft)
            pygame.draw.rect(screen, "grey", tile_rect, 3)
            draw_text(screen, font, str(tile_id), tile_rect.center)

