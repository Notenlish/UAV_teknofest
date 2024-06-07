import math
import os

import pygame


class Indicator:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area

        self.sky_col = config["indicatorSkyBackground"]
        self.ground_col = config["indicatorGroundBackground"]

        self.altitude_vel = 0
        self.rollORyawORpitch = 0 # hangisi bilmiyorum

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.sky_col,
            pygame.Rect(
                self.screen_area.x,
                self.screen_area.y,
                self.screen_area.w,
                self.screen_area.h // 2,
            ),
        )
        pygame.draw.rect(
            screen,
            self.ground_col,
            pygame.Rect(
                self.screen_area.x,
                self.screen_area.y + self.screen_area.h // 2,
                self.screen_area.w,
                self.screen_area.h // 2,
            ),
        )


if __name__ == "__main__":
    pass
