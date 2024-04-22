from kalman import ThetaKalmanFilter, VelocityKalmanFilter

from path_finding import PathFinding
from uav import OwnUAV, TargetUAV

import math


class Predictor:
    def __init__(
        self,
        theta_kalman: ThetaKalmanFilter,
        velocity_kalman: VelocityKalmanFilter,
        path_finding: PathFinding,
    ) -> None:
        self.theta_kalman = theta_kalman
        self.velocity_kalman = velocity_kalman
        self.path_finding = path_finding

    def run(self, measured_target_uav: TargetUAV):
        predicted_theta = self.theta_kalman.run(
            self.path_finding.measured_target_uav.theta
        )
        predicted_vel = self.velocity_kalman.run(
            self.path_finding.measured_target_uav.vel
        )
        new_x = (
            self.path_finding.predicted_target_uav.x
            + math.cos(predicted_theta) * predicted_vel
        )
        new_y = (
            self.path_finding.predicted_target_uav.y
            + math.sin(predicted_theta) * predicted_vel
        )
        self.path_finding.predicted_target_uav.x = new_x
        self.path_finding.predicted_target_uav.y = new_y
