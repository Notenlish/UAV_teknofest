from uav import OwnUAV, TargetUAV, DubinPoint

from path_maker import PathMaker


class Pathfinder:
    def __init__(self, own_uav_dub_pos, target_uav_dub_pos, turning_radius, step_size) -> None:
        
        self.own_uav_dub_pos: DubinPoint = own_uav_dub_pos
        self.target_uav_dub_pos: DubinPoint = target_uav_dub_pos
        self.own_uav_past_locations = []
        self.target_uav_past_locations = []
        self.predicted = None
        self.updated = None
        
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
            self.own_uav_dub_pos,
            self.target_uav_dub_pos,
            self.turning_radius,
            self.step_size,
        )

        results = {
            "own_uav": self.own_uav_dub_pos,
            "target_uav": self.target_uav_dub_pos,
            "own_uav_past_locations":self.own_uav_past_locations,
            "target_uav_past_locations":self.target_uav_past_locations,
            "predicted":self.predicted,
            "updated":self.updated,
            "path": path,
            "segments": segments,
        }
        return results
