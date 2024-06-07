import math
import os

import pygame
from geopy import distance

from utils import draw_table

from types import FunctionType


class TeamViewer:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area

        self.bg_col = config["windowBackground"]
        self.test_teams = config["testTeams"]

        self.altitude_vel = 0

    def render(self, screen, font):
        pygame.draw.rect(screen, self.bg_col, self.screen_area)

        table = [["ID", "ZF", "Mesafe", "Hız", "Tahmin", "Puan"]]
        for team in self.test_teams:
            _id = team["takim_numarasi"]
            latitude = team["iha_enlem"]
            longtitude = team["iha_boylam"]
            altitude = team["iha_irtifa"]
            bearing = team["iha_yonelme"]
            pitch = team["iha_dikilme"]  # elevation/depression angle
            roll = team["iha_yatis"]
            speed = team["iha_hizi"]
            time_diff_ms = team["zaman_farki"]

            # bizim okulun konumu
            coord_1 = (
                41.050833,
                29.008319,
            )  # TODO: change this later
            coord_2 = (latitude, longtitude)

            dist = distance.distance(coord_1, coord_2).kilometers  # TODO: change to meters

            table.append(
                [
                    str(_id),
                    str(f"{time_diff_ms / 1000:.1f}"),
                    str(f"{dist:.0f}"),
                    str(f"{speed:.0f}"),
                    str(20),
                    str(f"{altitude + bearing + pitch:.0f}"),
                ],
            )

        draw_table(
            screen,
            font,
            table,
            self.screen_area,
            text_color="black",
            sep_color="white",
        )


if __name__ == "__main__":
    pass
