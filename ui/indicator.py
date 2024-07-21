from math import sin, cos
import os

import pygame


class Indicator:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area

        self.sky_col = config["indicatorSkyBackground"]
        self.ground_col = config["indicatorGroundBackground"]

        self.altitude_vel = 0
        self.roll = 0  # rad

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

        rect = pygame.Rect(self.screen_area.centerx, self.screen_area.centery, 1, 1)

        bottom_start = rect.move(sin(self.roll) * line_sep, cos(self.roll) * line_sep)
        bottom_end = bottom_start.move(sin(self.roll) * line_w, cos(self.roll) * line_w)

        left_start = rect.move(cos(self.roll) * line_sep, sin(self.roll) * line_sep)
        left_end = left_start.move(cos(self.roll) * line_w, sin(self.roll) * line_w)

        right_start = rect.move(cos(self.roll) * -line_sep, sin(self.roll) * -line_sep)
        right_end = right_start.move(cos(self.roll) * -line_w, sin(self.roll) * -line_w)

        pygame.draw.line(screen, "red", left_start.center, left_end.center, width=3)
        pygame.draw.line(screen, "red", right_start.center, right_end.center, width=3)
        # pygame.draw.circle(screen, "blue", bottom_start.center, radius=2)
        # pygame.draw.circle(screen, "blue", bottom_end.center, radius=2)
        pygame.draw.line(screen, "red", bottom_start.center, bottom_end.center, width=3)


if __name__ == "__main__":
    pass
