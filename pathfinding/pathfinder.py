
from uav import OwnUAV, TargetUAV

from path_maker import PathMaker

class Pathfinder:
    def __init__(self, turning_radius, step_size) -> None:
        self.own_uav = OwnUAV(100, 100, theta=0)
        self.target_uav = TargetUAV(400, 300, theta=0)

        # NOTE when calculating paths, it should store 2 locations,
        # one for the location we got from the server and 
        # the other for the location that we assume the uav is in
        # (we calculate average vel. using kalman filter) and apply it by getting dt 
        # So it will basically calculate two paths
        self.pathmaker = PathMaker()

        self.turning_radius = turning_radius
        self.step_size = step_size
    
    def run(self, data: dict[str, any]):
        path, segments = self.pathmaker.run(self.own_uav.as_dubin_point(),
                           self.target_uav.as_dubin_point(),
                           self.turning_radius, self.step_size)

        results = {
            "self_uav": self.own_uav,
            "target_uav": self.target_uav,
            "path":path,
            "segments":segments,
        }
        return results