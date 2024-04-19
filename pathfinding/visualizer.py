import pygame

from shape import Point
from pydubins import DubinsPath

from uav import OwnUAV, TargetUAV
from camera import Camera

import math


# TODO the pathfinder will calculate two paths, one for the guessed location of target
# and the other for the location confirmed by server
# When drawing the paths and the uavs, keep this in mind


def add_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def subtract_tuple(t1, t2):
    return (t1[0] - t2[0], t1[1] - t2[1])


class Visualizer:
    def __init__(
        self, surface: pygame.Surface, camera: Camera, display: pygame.display
    ) -> None:
        self.surface = surface
        pygame.font.init()
        try:
            self.font = pygame.font.Font("pathfinding/Outfit-VariableFont_wght.ttf", 16)
        except FileNotFoundError:
            self.font = pygame.font.Font("Outfit-VariableFont_wght.ttf", 16)
        self.display = display
        self.camera = camera

        self.uav_rad = 15
        self.past_loc_rad = 5
        self.uav_dir_width = 4

    def draw_text(self, text, point: Point):
        surf = self.font.render(text)
        self.surface.blit(
            surf, subtract_tuple(point.get_tuple(), self.camera.get_pos())
        )

    def _draw_uavs(self, own_uav: OwnUAV, target_uav: TargetUAV):
        own_uav_pos = subtract_tuple(own_uav.get_pos(), self.camera.get_pos())
        target_uav_pos = subtract_tuple(target_uav.get_pos(), self.camera.get_pos())

        pygame.draw.circle(self.surface, "#8ECAE6", own_uav_pos, radius=self.uav_rad)
        pygame.draw.line(
            self.surface,
            "#219EBC",
            own_uav_pos,
            (
                own_uav_pos[0] + (math.cos(own_uav.theta) * self.uav_rad),
                own_uav_pos[1] + (math.sin(own_uav.theta) * self.uav_rad),
            ),
            width=self.uav_dir_width,
        )

        pygame.draw.circle(self.surface, "#EC4F62", target_uav_pos, radius=self.uav_rad)
        pygame.draw.line(
            self.surface,
            "#B81530",
            target_uav_pos,
            (
                target_uav_pos[0] + (math.cos(target_uav.theta) * self.uav_rad),
                target_uav_pos[1] + (math.sin(target_uav.theta) * self.uav_rad),
            ),
            width=self.uav_dir_width,
        )

    def _draw_past_locations(self, own_uav: OwnUAV, target_uav: TargetUAV):
        for loc in own_uav.past_locations:
            pygame.draw.circle(
                self.surface,
                "#D6C9C9",
                subtract_tuple(loc, self.camera.get_pos()),
                radius=self.past_loc_rad,
            )
        for loc in target_uav.past_locations:
            pygame.draw.circle(
                self.surface,
                "#C9CFD6",
                subtract_tuple(loc, self.camera.get_pos()),
                radius=self.past_loc_rad,
            )

    def draw(
        self,
        own_uav: OwnUAV,
        target_uav: TargetUAV,
        path: DubinsPath,
        segments: dict[str, any],
    ):
        self.surface.fill("#EBEBEB")

        self._draw_past_locations(own_uav, target_uav)
        self._draw_uavs(own_uav, target_uav)

        points = []
        for v in segments.values():
            point = subtract_tuple((v["q"][0], v["q"][1]), self.camera.get_pos())
            pygame.draw.circle(self.surface, "#8D99AE", point, radius=2)
            points.append(point)
        pygame.draw.lines(self.surface, "black", False, points, width=1)

        start_pos = subtract_tuple(
            (path.qi[0], path.qi[1]), self.camera.get_pos()
        )  # same as just getting own_uav.get_pos()
        end_pos = subtract_tuple((target_uav.get_pos()), self.camera.get_pos())
        # for some reason the path object doesnt have end path
        pygame.draw.circle(self.surface, "black", start_pos, radius=2)
        pygame.draw.circle(self.surface, "black", end_pos, radius=2)

        self.display.update()
