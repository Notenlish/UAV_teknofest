from math import sin, cos
import os

import pygame


class Indicator:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area

        self.sky_col = config["indicatorSkyBackground"]
        self.ground_col = config["indicatorGroundBackground"]

        self.altitude_vel = 0
        self.roll = 0.5  # rad

    def _draw_bg(self, screen):
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

    def render(self, screen: pygame.Surface):
        self._draw_bg(screen)
        pixel_percent_w = self.screen_area.w / 100
        pixel_percent_h = self.screen_area.h / 100

        line_w = 10 * pixel_percent_w
        line_sep = 10 * pixel_percent_w

        low_left = self.screen_area.move(
            -5 * pixel_percent_w, 5 * pixel_percent_h
        ).center
        low_right = self.screen_area.move(
            5 * pixel_percent_w, 5 * pixel_percent_h
        ).center

        left_start = self.screen_area.move(
            cos(self.roll) * line_sep, sin(self.roll) * line_sep
        )
        left_end = left_start.move(cos(self.roll) * line_w, sin(self.roll) * line_w)

        right_start = self.screen_area.move(
            cos(self.roll) * -line_sep, sin(self.roll) * -line_sep
        )
        right_end = right_start.move(cos(self.roll) * -line_w, sin(self.roll) * -line_w)

        pygame.draw.line(screen, "red", left_start.center, left_end.center, width=3)
        pygame.draw.line(screen, "red", right_start.center, right_end.center, width=3)
        pygame.draw.lines(
            screen,
            "red",
            closed=False,
            points=[low_left, self.screen_area.center, low_right],
            width=3,
        )


if __name__ == "__main__":
    pass
