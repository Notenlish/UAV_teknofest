import pygame

from shape import Point
from pydubins import DubinsPath

import json


class Visualizer:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 16)

    def draw_text(self, text, point: Point):
        surf = self.font.render(text)
        self.surface.blit(surf, point.get_tuple())

    def draw(
        self,
        result_path: DubinsPath,
        sample_results: dict[float, dict[str, list[float, 3] | dict]],
    ):
        self.surface.fill("#EBEBEB")
        
        points = []
        for v in sample_results.values():
            point = (v["q"][0], v["q"][1])
            pygame.draw.circle(self.surface, "black", point, radius=2)
            points.append(point)
        pygame.draw.lines(self.surface, "black", False, points, width=1)