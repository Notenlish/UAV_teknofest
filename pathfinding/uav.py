from shape import DubinPoint
from enum import Enum


class UAVPredictColors:
    own = {"bg_col": "#8E9AE6", "dir_col": "#2253BD"}
    target = {"bg_col": "#ED794E", "dir_col": "#B84D14"}


class UAV:
    def __init__(self, x, y, theta, vel=50, past_locations=[]) -> None:
        self.x = x
        self.y = y
        self.vel = vel
        self.past_locations: list[tuple[float, float]] = past_locations
        self.theta = theta

        self.bg_col = "#E0E0E0"
        self.dir_col = "#C2C2C2"

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


class TargetUAV(UAV):
    def __init__(self, x, y, theta, vel=50, past_locations=[]) -> None:
        super().__init__(x, y, theta, vel, past_locations)
        self.turnfor = 0
        self.waitfor = 0
        self.time_waited = 0
        self.since_last_pos_save = 0
        self.bg_col = "#EC4F62"
        self.dir_col = "#B81530"
