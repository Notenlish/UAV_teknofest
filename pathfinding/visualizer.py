import pygame

from shape import Point
from pydubins import DubinsPath

from uav import OwnUAV, TargetUAV

import math

class Visualizer:
    def __init__(self, surface: pygame.Surface, display: pygame.display) -> None:
        self.surface = surface
        pygame.font.init()
        try:
            self.font = pygame.font.Font("pathfinding/Outfit-VariableFont_wght.ttf", 16)
        except FileNotFoundError:
            self.font = pygame.font.Font("Outfit-VariableFont_wght.ttf", 16)
        self.display = display

        self.uav_rad = 15
        self.uav_dir_width = 4

    def draw_text(self, text, point: Point):
        surf = self.font.render(text)
        self.surface.blit(surf, point.get_tuple())

    def _draw_uavs(self, own_uav: OwnUAV, target_uav: TargetUAV):
        own_uav_pos = own_uav.get_pos()
        target_uav_pos = target_uav.get_pos()

        pygame.draw.circle(self.surface, "#8ECAE6", own_uav_pos, radius=self.uav_rad)
        pygame.draw.line(self.surface, "#219EBC", own_uav_pos, (
            own_uav_pos[0] + (math.sin(own_uav.theta) * self.uav_rad),
            own_uav_pos[1] + (math.cos(own_uav.theta) * self.uav_rad)), width=self.uav_dir_width)
        
        pygame.draw.circle(self.surface, "#EC4F62", target_uav.get_pos(), radius=self.uav_rad)
        pygame.draw.line(self.surface, "#B81530", target_uav_pos, (
            target_uav_pos[0] + (math.sin(target_uav.theta) * self.uav_rad),
            target_uav_pos[1] + (math.cos(target_uav.theta) * self.uav_rad)), width=self.uav_dir_width)

    def draw(
        self,
        own_uav: OwnUAV,
        target_uav: TargetUAV,
        path: DubinsPath,
        segments: dict[str, any]
    ):
        self.surface.fill("#EBEBEB")

        self._draw_uavs(own_uav, target_uav)

        points = []
        for v in segments.values():
            point = (v["q"][0], v["q"][1])
            pygame.draw.circle(self.surface, "#8D99AE", point, radius=2)
            points.append(point)
        pygame.draw.lines(self.surface, "black", False, points, width=1)

        start_pos = (path.qi[0], path.qi[1])  # same as just getting own_uav.get_pos()
        end_pos = target_uav.get_pos()  # for some reason the path object doesnt have end path
        pygame.draw.circle(self.surface, "black", start_pos, radius=2)
        pygame.draw.circle(self.surface, "black", end_pos, radius=2)

        self.display.update()