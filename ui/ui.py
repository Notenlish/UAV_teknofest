import pygame
from threading import Event

from sys import getsizeof
from functools import lru_cache

from geopy import distance

from typing import Literal

from random import randint

try:
    from utils import hash_pg_rect
except ModuleNotFoundError:
    pass

pygame.font.init()


class UI:
    def __init__(self, config: dict[str, any]) -> None:
        self.screen_size = config["windowSize"]
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.UI_FPS = config["windowFPS"]
        self.is_running = False

        self.earth_move_speed = config["earthMoveSpeed"]
        self.earth = pygame.image.load(
            "ui/earth.jpg"
        ).convert()  # https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74518/world.topo.200412.3x21600x10800.jpg

        self.zoom_steps = config["earthZoomSteps"]
        self.test_teams = config["testTeams"]

        self.font = pygame.font.Font("ui/Renogare-Regular.otf", size=20)
        pygame.transform.set_smoothscale_backend("SSE2")

    def _draw_teams(self, MEMORY):
        pixel_percent_w = self.screen_size[0] / 100
        pixel_percent_h = self.screen_size[1] / 100
        teams_screen_area = pygame.Rect(
            50 * pixel_percent_w, 0, 35 * pixel_percent_w, 60 * pixel_percent_h
        )
        pygame.draw.rect(self.screen, "green", teams_screen_area)

        start_pos = list(teams_screen_area.topleft)
        self._draw_texts(
            ["ID", "Zaman Farkı", "Mesafe", "Hız", "Tahmin", "Puan"],
            teams_screen_area.topleft,
            anchor=("left", "top"),
        )
        for team in self.test_teams:
            start_pos[1] += 25

            _id = team["takim_numarasi"]
            latitude = team["iha_enlem"]
            longtitude = team["iha_boylam"]
            altitude = team["iha_irtifa"]
            bearing = team["iha_yonelme"]
            pitch = team["iha_dikilme"]  # + if going up, - if going down
            roll = team["iha_yatis"]
            speed = team["iha_hizi"]
            time_diff_ms = team["zaman_farki"]

            # bizim okulun konumu
            coord_1 = (
                41.050833,
                29.008319,
            )  # TODO: change this later
            coord_2 = (latitude, longtitude)

            dist = distance.distance(coord_1, coord_2).meters

            # TODO: fix this
            self._draw_texts(
                [
                    str(_id),
                    str(time_diff_ms),
                    str(f"{dist:.2f}"),
                    str(f"{speed:.2f}"),
                    str(20),
                    str(f"{altitude + bearing + pitch:.2f}"),
                ],
                start_pos,
                anchor=("left", "top"),
            )

    def _position_anchor(
        self, rect: pygame.Rect | pygame.FRect, anchor: tuple[str, str]
    ):
        resulty = None
        resultx = None
        if anchor[0] == "left":
            resultx = rect.left
        if anchor[0] == "center":
            resultx = -rect.centerx
        if anchor[0] == "right":
            resultx = -rect.right

        if anchor[1] == "top":
            resulty = rect.top
        if anchor[1] == "center":
            resulty = -rect.centery
        if anchor[1] == "bottom":
            resulty = rect.bottom

        return (resultx, resulty)

    def _set_zoom(self, MEMORY: dict[str, any]):
        MEMORY["zoom"] = min(max(MEMORY["zoom"], 0), 9)
        val = self.zoom_steps[MEMORY["zoom"]]
        result_zoom = 1 / val
        print(MEMORY["zoom"], val)

        orig = MEMORY["orig_earth_rect"].copy()
        MEMORY["orig_earth_rect"].scale_by_ip(result_zoom)
        x = MEMORY["earth_rect"].centerx
        y = MEMORY["earth_rect"].centery
        MEMORY["earth_rect"] = MEMORY["orig_earth_rect"]
        MEMORY["earth_rect"].centerx = x
        MEMORY["earth_rect"].centery = y
        MEMORY["orig_earth_rect"] = orig

    def _draw_earth(self, MEMORY):
        pixel_percent_w = self.screen_size[0] / 100
        pixel_percent_h = self.screen_size[1] / 100
        earth_screen_area = pygame.Rect(
            0,
            0,
            round(pixel_percent_w * 50),
            round(pixel_percent_h * 60),
        )
        rect: pygame.Rect = MEMORY["earth_rect"]
        if rect.w < 0 or rect.h < 0:
            return
        hashed_rect = hash_pg_rect(rect)
        # print(rect)
        try:
            result = MEMORY["earth_draw_cache"][hashed_rect]
            # print("found hashed")
        except KeyError:
            result = pygame.transform.smoothscale(
                self.earth.subsurface(rect).copy(), earth_screen_area.size
            )
            MEMORY["earth_draw_cache"][hashed_rect] = result
            # print(f"{getsizeof(MEMORY['earth_draw_cache']) / 1024 / 1024:.5f}")
        self.screen.blit(result, (0, 0))

    def move_earth(self, MEMORY: dict[str, any], x, y):
        rect: pygame.Rect = MEMORY["earth_rect"]
        pixel_per_percent = rect.w / 100
        rect = rect.move(
            x * self.earth_move_speed * pixel_per_percent,
            y * self.earth_move_speed * pixel_per_percent,
        )
        rect = rect.clamp(MEMORY["orig_earth_rect"])
        MEMORY["earth_rect"] = rect

    def _draw_texts(
        self,
        texts: list[str],
        start_point: tuple[float, float],
        color="black",
        anchor: tuple[str, str] = ("center", "center"),
        seperator: tuple[int, int] = (10, 0),
        move_dir: tuple[int, int] = (1, 0),
    ):
        pos = [*start_point]
        for text in texts:
            rect = self._draw_text(text, pos, color, anchor)
            pos[0] += rect.w * move_dir[0] + seperator[0]
            pos[1] += rect.h * move_dir[1] + seperator[1]
        return pos

    def _draw_text(
        self,
        text,
        point: tuple[float, float],
        color="black",
        anchor: tuple[str, str] = ("center", "center"),
    ):
        if type(text) != bytes and type(text) != str:
            text = str(text)
        surf = self.font.render(text, antialias=True, color=color)
        rect = surf.get_rect()
        anchor = self._position_anchor(rect, anchor)
        anchor = (anchor[0] + point[0], anchor[1] + point[1])
        self.screen.blit(surf, anchor)
        return rect

    def start(self, MEMORY: dict[str, any], EVENTS: dict[str, Event]):
        self.is_running = True
        MEMORY["earth_scaled"] = {}
        MEMORY["orig_earth_rect"] = pygame.Rect(self.earth.get_rect())
        MEMORY["earth_rect"] = MEMORY["orig_earth_rect"].copy()
        MEMORY["earth_draw_cache"] = {}
        MEMORY["zoom"] = 0
        while self.is_running:
            self.screen.fill("white")

            self._draw_earth(MEMORY)
            self._draw_text(
                f"{MEMORY['i']}", (self.screen_size[0] * 0.5, self.screen_size[1] * 0.5)
            )
            self._draw_teams(MEMORY)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        MEMORY["zoom"] += 1
                        self._set_zoom(MEMORY)
                    if event.key == pygame.K_F2:
                        MEMORY["zoom"] -= 1
                        self._set_zoom(MEMORY)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    EVENTS["close_app"].set()
                    break

            events = pygame.key.get_pressed()
            if events[pygame.K_w]:
                self.move_earth(MEMORY, 0, -1)
            if events[pygame.K_a]:
                self.move_earth(MEMORY, -1, 0)
            if events[pygame.K_s]:
                self.move_earth(MEMORY, 0, 1)
            if events[pygame.K_d]:
                self.move_earth(MEMORY, 1, 0)

            self.dt = self.clock.tick(self.UI_FPS)
            pygame.display.update()


# couldnt figure out how to set project launch json, so this is how I will be able to launch app.py from ui.py
if __name__ == "__main__":
    import os
    import sys

    current_directory = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.dirname(current_directory)

    sys.path.append(parent_directory)

    from app import App
    from utils import hash_pg_rect

    app = App()
    app.run()
