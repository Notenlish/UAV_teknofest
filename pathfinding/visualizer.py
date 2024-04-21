import math

import pygame
from camera import Camera
from pydubins import DubinsPath
from shape import Point
from uav import DubinPoint, OwnUAV, TargetUAV

# TODO the pathfinder will calculate two paths, one for the guessed location of target
# and the other for the location confirmed by server
# When drawing the paths and the uavs, keep this in mind
from utils import subtract_tuple


class Visualizer:
    def __init__(
        self, surface: pygame.Surface, camera: Camera, display: pygame.display
    ) -> None:
        self.surface = surface
        pygame.font.init()
        try:
            self.font = pygame.font.Font("pathfinding/Renogare-Regular.otf", 16)
        except FileNotFoundError:
            self.font = pygame.font.Font("Renogare-Regular.otf", 16)
        self.display = display
        self.camera = camera

        self.uav_rad = 16
        self.past_loc_rad = 5
        self.uav_dir_width = 5

    def draw_text(self, text, point: tuple[float, float], color="black"):
        surf = self.font.render(text, antialias=True, color=color)
        self.surface.blit(surf, point)

    def _draw_uavs(self, cam_pos, own_uav: DubinPoint, target_uav: DubinPoint):
        own_uav_campos = subtract_tuple(own_uav, cam_pos)
        target_uav_campos = subtract_tuple(target_uav.get_pos(), cam_pos)

        pygame.draw.circle(self.surface, "#8ECAE6", own_uav_campos, radius=self.uav_rad)
        self.draw_text(
            own_uav.get_pos_text(),
            subtract_tuple(own_uav_campos, (self.uav_rad, self.uav_rad + 20)),
        )
        pygame.draw.line(
            self.surface,
            "#219EBC",
            own_uav_campos,
            (
                own_uav_campos[0] + (math.cos(own_uav.theta) * self.uav_rad),
                own_uav_campos[1] + (math.sin(own_uav.theta) * self.uav_rad),
            ),
            width=self.uav_dir_width,
        )

        pygame.draw.circle(
            self.surface, "#EC4F62", target_uav_campos, radius=self.uav_rad
        )
        self.draw_text(
            target_uav.get_pos_text(),
            subtract_tuple(target_uav_campos, (self.uav_rad, self.uav_rad + 20)),
        )
        pygame.draw.line(
            self.surface,
            "#B81530",
            target_uav_campos,
            (
                target_uav_campos[0] + (math.cos(target_uav.theta) * self.uav_rad),
                target_uav_campos[1] + (math.sin(target_uav.theta) * self.uav_rad),
            ),
            width=self.uav_dir_width,
        )

    def _draw_past_locations(
        self,
        cam_pos,
        own_uav_past_locations: list[DubinPoint],
        target_uav_past_locations,
    ):
        for loc in own_uav_past_locations:
            pygame.draw.circle(
                self.surface,
                "#D6C9C9",
                subtract_tuple(loc, cam_pos),
                radius=self.past_loc_rad,
            )
        for loc in target_uav_past_locations:
            pygame.draw.circle(
                self.surface,
                "#C9CFD6",
                subtract_tuple(loc, cam_pos),
                radius=self.past_loc_rad,
            )

    def _draw_path(self, cam_pos, segments, own_uav, target_uav):
        points = []
        for v in segments.values():
            point = subtract_tuple(v["q"], cam_pos)
            # pygame.draw.circle(self.surface, "#8D99AE", point, radius=0)
            points.append(point)
        points.append(subtract_tuple(target_uav.get_pos(), cam_pos))
        pygame.draw.lines(self.surface, "black", False, points, width=1)

        start_pos = subtract_tuple(own_uav.get_pos(), cam_pos)
        # same as this:
        # subtract_tuple( (path.qi[0], path.qi[1]), cam_pos)

        end_pos = subtract_tuple((target_uav.get_pos()), cam_pos)
        # for some reason the path object doesnt have end path
        pygame.draw.circle(self.surface, "black", start_pos, radius=2)
        pygame.draw.circle(self.surface, "black", end_pos, radius=2)

    def _draw_prediction(self, cam_pos, predicted, updated):
        if updated:
            pygame.draw.circle(
                self.surface,
                "purple",
                subtract_tuple(updated.get_pos(), cam_pos),
                radius=self.uav_rad,
            )
        if predicted:
            pygame.draw.circle(
                self.surface,
                "pink",
                subtract_tuple(predicted.get_pos(), cam_pos),
                radius=self.uav_rad,
            )

    def draw(
        self,
        own_uav: DubinPoint,
        target_uav: DubinPoint,
        own_uav_past_locations: list[DubinPoint],
        target_uav_past_locations: list[DubinPoint],
        predicted: DubinPoint,
        updated: DubinPoint,
        path: DubinsPath,
        segments: dict[str, any],
    ):
        self.surface.fill("#EBEBEB")

        cam_pos = self.camera.get_pos()

        self._draw_past_locations(
            cam_pos, own_uav_past_locations, target_uav_past_locations
        )
        self._draw_uavs(cam_pos, own_uav, target_uav)

        self._draw_path(cam_pos, segments, own_uav, target_uav)

        self._draw_prediction(cam_pos, predicted, updated)

        self.display.update()
