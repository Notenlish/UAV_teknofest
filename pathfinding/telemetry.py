import math
from random import choice, random

from path_finding import PathFinding
from uav import OwnUAV, TargetUAV, UAVPredictColors
from utils import add_tuple
from predictor import Predictor

from copy import deepcopy

# TODO more than 1 target uav data being given by telemetry


class Telemetry:
    def __init__(self, own_uav: OwnUAV, target_uav: TargetUAV) -> None:
        self.own_uav = own_uav
        self.target_uav = target_uav

        self.will_keep_player_near = True
        self.server_wait_time = 1

        self.path_finding: PathFinding = None
        self.predictor: Predictor = None

        self.waited = self.server_wait_time

    def init(self, path_finding: PathFinding, predictor: Predictor):
        self.path_finding = path_finding
        self.predictor: Predictor = predictor

    def set_own_uav_theta(self, cam_pos, mouse_pos):
        pos = add_tuple(mouse_pos, cam_pos)
        diffx = pos[0] - self.own_uav.x
        diffy = pos[1] - self.own_uav.y
        theta = math.atan2(diffy, diffx)
        self.own_uav.theta = theta

    def change_target_movement(self):
        if self.target_uav.time_waited >= self.target_uav.waitfor:  # seconds
            print(f"{self.target_uav.waitfor:.2f} seconds passed")
            self.time_passed = 0

            _rot_dir = choice([-1, 1])
            self.target_uav.turnfor = ((random() * 0.7) + 0.05) * _rot_dir

            self.target_uav.waitfor = (random() * 2) + 2
            self.target_uav.time_waited = 0
            self.target_uav.since_last_pos_save = 0

    def keep_player_near(self, time_passed_s: float):
        dist_x = self.target_uav.x - self.own_uav.x
        dist_y = self.target_uav.y - self.own_uav.y
        if self.will_keep_player_near and math.sqrt(dist_x**2 + dist_y**2) > 400:
            self.own_uav.x += dist_x * 0.1 * time_passed_s
            self.own_uav.y += dist_y * 0.1 * time_passed_s

    def save_target_last_pos(self, time_passed_s: float):
        self.target_uav.since_last_pos_save -= time_passed_s
        if self.target_uav.since_last_pos_save <= 0:
            self.target_uav.past_locations.append(self.target_uav.get_pos())
            self.target_uav.since_last_pos_save = 0.5  # seconds

    def move_target(self, time_passed_s: float):
        self.target_uav.theta += self.target_uav.turnfor * time_passed_s
        self.target_uav.x += (
            math.cos(self.target_uav.theta) * self.target_uav.vel * time_passed_s
        )
        self.target_uav.y += (
            math.sin(self.target_uav.theta) * self.target_uav.vel * time_passed_s
        )

    def send_target_pos(self, time_passed_s):
        self.waited += time_passed_s
        if self.waited >= self.server_wait_time:
            self.waited = 0

            self.path_finding.own_uav_past_locations.append(
                self.path_finding.measured_own_uav.get_pos()
            )
            self.path_finding.target_uav_past_locations.append(
                self.path_finding.measured_target_uav.get_pos()
            )
            self.path_finding.measured_own_uav = deepcopy(self.own_uav)
            self.path_finding.predicted_own_uav = deepcopy(self.own_uav)
            self.path_finding.measured_target_uav = deepcopy(self.target_uav)
            self.path_finding.predicted_target_uav = deepcopy(self.target_uav)
            
            self.path_finding.predicted_own_uav.bg_col = UAVPredictColors.own["bg_col"]
            self.path_finding.predicted_own_uav.dir_col = UAVPredictColors.own["dir_col"]
            self.path_finding.predicted_target_uav.bg_col = UAVPredictColors.target["bg_col"]
            self.path_finding.predicted_target_uav.dir_col = UAVPredictColors.target["dir_col"]
                

            self.predictor.run(self.target_uav)

    def run(self, dt):
        time_passed_s = dt / 1000
        self.target_uav.time_waited += time_passed_s

        self.keep_player_near(time_passed_s)

        self.change_target_movement()
        self.save_target_last_pos(time_passed_s)

        self.move_target(time_passed_s)

        self.send_target_pos(time_passed_s)
