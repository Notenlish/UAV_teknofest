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

        self.bg_col = config["windowBackground"]
        self.window_size = config["windowSize"]

        self.debug = True

        self.camera_x = 0
        self.camera_y = 0

    def _calculate_max_tiles(self):
        self.max_tile_nums = 2**self.zoom if self.zoom != 0 else 1

    def move(self, x, y, dt):
        tile_w = 256 * self.scale
        tile_h = 256 * self.scale

        self.camera_x += x * self.earth_move_speed * dt
        self.camera_y += y * self.earth_move_speed * dt

        val = self.zoom if self.zoom != 0 else 1
        # usta neden bunu yapmamız gerektiğini bilmiyoruz, ama lazım
        # yoksa harita dışına çıkabiliyorsun
        # elleme sakın.
        # elleyen gay.
        if self.zoom % 2 == 1:  # odd number
            val = 2

        self.camera_x = min(max(self.camera_x, 0), (self.max_tile_nums - val) * tile_w)
        self.camera_y = min(max(self.camera_y, 0), (self.max_tile_nums - val + 0.29) * tile_h)

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

        offset_x = self.camera_x % tile_w
        offset_y = self.camera_y % tile_h

        tile_start_x = int(self.camera_x) // tile_w
        tile_start_y = int(self.camera_y) // tile_h

        how_many_rects_hor = (int(self.screen_area.width) // tile_w) + 1 
        how_many_rects_ver = (int(self.screen_area.height) // tile_h) + 2

        tile_end_x = tile_start_x + how_many_rects_hor

        tile_diff_x = tile_start_x
        tile_diff_y = tile_start_y

        if self.zoom == 0:
            tile_end_x = 1

        tile_end_y = tile_start_y + how_many_rects_ver

        if self.zoom == 0:
            tile_end_y = 1

        tiles = []
        for y in range(tile_start_y, tile_end_y):
            for x in range(tile_start_x, tile_end_x):
                tile_id = x + y * self.max_tile_nums

                normalized_tile_x = x - tile_diff_x
                normalized_tile_y = y - tile_diff_y

                screen_x = 0 + normalized_tile_x * tile_w - offset_x
                screen_y = 0 + normalized_tile_y * tile_h - offset_y

                tile = {
                    "x": screen_x,
                    "y": screen_y,
                    "w": tile_w,
                    "h": tile_h,
                    "tile_x": x % self.max_tile_nums,
                    "tile_y": y % self.max_tile_nums,
                }
                tiles.append(tile)
        return tiles

    def render(self, screen: pygame.Surface, font: pygame.Font):
        for tile in self.calculate_tiles(screen, font):
            tile_rect = pygame.Rect(tile["x"], tile["y"], tile["w"], tile["h"])
            tile_x = tile["tile_x"]
            tile_y = tile["tile_y"]

            # print(
            #    f"id:{tile_id} x:{tile_x} y:{tile_y} maxX:{max_tile_x} maxY:{max_tile_y}"
            # )

            img = self.load_tile(self.zoom, tile_x, tile_y)

            screen.blit(img, tile_rect.topleft)
            if self.debug:
                pygame.draw.rect(screen, "grey", tile_rect, 3)
                draw_text(
                screen, font, f"x{tile_x} y{tile_y}", tile_rect.center, color="red"
                )
        pygame.draw.rect(
            screen,
            self.bg_col,
            pygame.Rect(
                0,
                self.screen_area.h,
                self.window_size[0],
                self.window_size[1] - self.screen_area.h,
            ),
        )
