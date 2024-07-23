from shape import DubinPoint


class UAVPredictColors:
    own = {"bg_col": "#8E9AE6", "dir_col": "#2253BD", "past_loc_col": "#C7CBE2"}
    target = {"bg_col": "#ED794E", "dir_col": "#D95812", "past_loc_col": "#E1C6BC"}


class UAV:
    def __init__(self, x, y, theta, vel=50, past_locations=[]) -> None:
        self.x = x
        self.y = y
        self.vel = vel
        self.past_locations: list[tuple[float, float]] = past_locations
        self.theta = theta
        self.since_last_pos_save = 0

        self.bg_col = "#E0E0E0"
        self.dir_col = "#C2C2C2"
        self.past_loc_col = "#949396"

    def update(self, uav):
        """Used for updating the predicted uav instances in telemetry module."""
        self.x = uav.x
        self.y = uav.y
        self.vel = uav.vel
        self.theta = uav.theta

    def get_pos(self):
        return (self.x, self.y)

    def get_pos_text(self):
        # add .2f if you want
        return f"({self.x:.0f}, {self.y:.0f})"

    def as_dubin_point(self):
        return DubinPoint(self.x, self.y, self.theta)


class OwnUAV(UAV):
    def __init__(self, x, y, theta, vel=50, past_locations=[]) -> None:
        super().__init__(x, y, theta, vel, past_locations)
        self.bg_col = "#8ECAE6"
        self.dir_col = "#219EBC"
        self.past_loc_col = "#CFDBE1"


class TargetUAV(UAV):
    def __init__(self, x, y, theta, vel=50, past_locations=[]) -> None:
        super().__init__(x, y, theta, vel, past_locations)
        self.turnfor = 0
        self.waitfor = 0
        self.time_waited = 0
        self.bg_col = "#EC4F62"
        self.dir_col = "#B81530"
        self.past_loc_col = "#E7D2D5"


if __name__ == "__main__":
    a = TargetUAV(0, 0, 0)
    import sys

    for v in range(1_000_000):
        a.past_locations.append((v + 1, v + 1))
    size = sys.getsizeof(a.past_locations) / (1024 * 1024.0)
    print(size)
    # 1 million locations = 8 mb so idk mem will be an issue
