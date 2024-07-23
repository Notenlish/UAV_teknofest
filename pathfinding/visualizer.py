import math

import pygame
from camera import Camera
from uav import UAV
from path_finding import PathFinding

# TODO the pathfinder will calculate two paths, one for the guessed location of target
# and the other for the location confirmed by server
# When drawing the paths and the uavs, keep this in mind
from utils import subtract_tuple, add_tuple, multiply_tuple_by_int


class Visualizer:
    def __init__(
        self, surface: pygame.Surface, camera: Camera, display: pygame.display
    ) -> None:
        self.surface = surface
        pygame.font.init()

        self.display = display
        self.camera = camera

        self.is_debug = False

        self.uav_rad = 16
        self.past_loc_rad = 5
        self.uav_dir_width = 5
        self.font_size = 14

        try:
            self.font = pygame.font.Font(
                "pathfinding/Renogare-Regular.otf", self.font_size
            )
        except FileNotFoundError:
            self.font = pygame.font.Font("Renogare-Regular.otf", self.font_size)

        self.path_finding = None

    def init(self, path_finding: PathFinding):
        self.path_finding = path_finding

    def _draw_target_theta(self):
        center = (50, 50)  # topleft
        target_m_line_pos = (
            math.cos(self.path_finding.measured_target_uav.theta) * 40,
            math.sin(self.path_finding.measured_target_uav.theta) * 40,
        )
        target_p_line_pos = (
            math.cos(self.path_finding.predicted_target_uav.theta) * 40,
            math.sin(self.path_finding.predicted_target_uav.theta) * 40,
        )
        pygame.draw.line(
            self.surface,
            self.path_finding.measured_target_uav.dir_col,
            center,
            add_tuple(center, target_m_line_pos),
            width=4,
        )
        pygame.draw.line(
            self.surface,
            self.path_finding.predicted_target_uav.dir_col,
            center,
            add_tuple(center, target_p_line_pos),
            width=4,
        )

    def draw_text(self, text, point: tuple[float, float], color="black"):
        surf = self.font.render(text, antialias=True, color=color)
        self.surface.blit(surf, point)

    def _draw_uavs(self, time_left, server_wait_time):
        measured_uavs = [
            self.path_finding.measured_own_uav,
            self.path_finding.measured_target_uav,
        ]
        predicted_uavs = [
            self.path_finding.predicted_own_uav,
            self.path_finding.predicted_target_uav,
        ]
        for i, m_uav in enumerate(measured_uavs):
            m_uav: UAV
            p_uav: UAV = predicted_uavs[i]

            # predicted uav
            if self.is_debug:
                diff = subtract_tuple(p_uav.get_pos(), m_uav.get_pos())
                ratio = time_left / server_wait_time
                predicted_pos = add_tuple(
                    m_uav.get_pos(), multiply_tuple_by_int(ratio, diff)
                )
                predicted_cam_pos = subtract_tuple(predicted_pos, self.camera.get_pos())
                pygame.draw.circle(
                    self.surface,
                    p_uav.bg_col,
                    predicted_cam_pos,
                    self.uav_rad,
                )
                pygame.draw.line(
                    self.surface,
                    p_uav.dir_col,
                    predicted_cam_pos,
                    add_tuple(
                        predicted_cam_pos,
                        (
                            math.cos(p_uav.theta) * self.uav_rad,
                            math.sin(p_uav.theta) * self.uav_rad,
                        ),
                    ),
                    width=self.uav_dir_width,
                )

            # info
            if self.is_debug:
                self.draw_text(
                    f"p: {m_uav.get_pos_text()}\n p_p:{p_uav.get_pos_text()}\nt: {m_uav.theta:.2f}\np_t: {p_uav.theta:.2f}",
                    subtract_tuple(
                        subtract_tuple(m_uav.get_pos(), self.camera.get_pos()),
                        (self.uav_rad, self.uav_rad + 70),
                    ),
                )

            # measured uav
            m_uav_cam_pos = subtract_tuple(m_uav.get_pos(), self.camera.get_pos())
            pygame.draw.circle(
                self.surface, m_uav.bg_col, m_uav_cam_pos, self.uav_rad
            )  # body
            pygame.draw.line(
                self.surface,
                m_uav.dir_col,
                m_uav_cam_pos,
                add_tuple(
                    m_uav_cam_pos,
                    (
                        math.cos(m_uav.theta) * self.uav_rad,
                        math.sin(m_uav.theta) * self.uav_rad,
                    ),
                ),
                width=self.uav_dir_width,
            )  # dir

    def _draw_past_locations(self):
        cam_pos = self.camera.get_pos()
        measured_uavs = [
            self.path_finding.measured_own_uav,
            self.path_finding.measured_target_uav,
        ]
        predicted_uavs = [
            self.path_finding.predicted_own_uav,
            self.path_finding.predicted_target_uav,
        ]
        for l in [measured_uavs, predicted_uavs]:
            for i, v in enumerate(l):
                v: UAV
                for loc in v.past_locations:
                    pygame.draw.circle(
                        self.surface,
                        v.past_loc_col,
                        subtract_tuple(loc, cam_pos),
                        radius=self.past_loc_rad,
                    )

    def _draw_path(self, path, segments):
        cam_pos = self.camera.get_pos()
        points = []
        r = 2
        for v in segments.values():
            point = subtract_tuple(v["q"], cam_pos)
            pygame.draw.circle(self.surface, "#8D99AE", point, radius=r)
            points.append(point)
        points.append(
            subtract_tuple(self.path_finding.measured_target_uav.get_pos(), cam_pos)
        )
        pygame.draw.lines(self.surface, "black", False, points, width=1)

        start_pos = subtract_tuple(
            self.path_finding.measured_own_uav.get_pos(), cam_pos
        )
        # same as this:
        # subtract_tuple( (path.qi[0], path.qi[1]), cam_pos)

        end_pos = subtract_tuple(
            (self.path_finding.measured_target_uav.get_pos()), cam_pos
        )
        # for some reason the path object doesnt have end path
        pygame.draw.circle(self.surface, "black", start_pos, radius=2)
        pygame.draw.circle(self.surface, "black", end_pos, radius=2)

    def _draw_prediction(self):
        pass

    def draw(self, time_left: float, server_wait_time: float, path, segments):
        self.surface.fill("#EBEBEB")
        if self.is_debug:
            self._draw_past_locations()
        self._draw_uavs(time_left, server_wait_time)

        self._draw_path(path, segments)

        self._draw_prediction()

        if self.is_debug:
            self._draw_target_theta()

        self.display.update()
