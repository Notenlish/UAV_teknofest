from path_maker import PathMaker
from uav import DubinPoint, OwnUAV, TargetUAV, UAVPredictColors
from copy import deepcopy


class PathFinding:
    def __init__(
        self, measured_own_uav, measured_target_uav, turning_radius, step_size
    ) -> None:

        self.measured_own_uav: OwnUAV = measured_own_uav
        self.measured_target_uav: TargetUAV = measured_target_uav
        self.own_uav_past_locations = []
        self.target_uav_past_locations = []

        self.predicted_own_uav: OwnUAV = deepcopy(measured_own_uav)
        print(UAVPredictColors.own)
        self.predicted_own_uav.bg_col = UAVPredictColors.own["bg_col"]
        self.predicted_own_uav.dir_col = UAVPredictColors.own["dir_col"]
        self.predicted_target_uav: TargetUAV = deepcopy(measured_target_uav)
        self.predicted_target_uav.bg_col = UAVPredictColors.target["bg_col"]
        self.predicted_target_uav.dir_col = UAVPredictColors.target["dir_col"]

        # NOTE when calculating paths, it should store 2 locations,
        # one for the location we got from the server and
        # the other for the location that we assume the uav is in
        # (we calculate average vel. using kalman filter) and apply it by getting dt
        # So it will basically calculate two paths
        self.pathmaker = PathMaker()

        self.turning_radius = turning_radius
        self.step_size = step_size

    def run(self):
        path, segments = self.pathmaker.run(
            self.measured_own_uav,
            self.measured_target_uav,
            self.turning_radius,
            self.step_size,
        )
        return path, segments
