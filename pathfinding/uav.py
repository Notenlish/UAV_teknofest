from shape import DubinPoint


class UAV:
    def __init__(self, x, y, theta, calculated_vel=None, past_locations=[]) -> None:
        self.x = x
        self.y = y
        self.calculated_vel = calculated_vel
        self.past_locations: list[tuple[float, float]] = past_locations
        self.theta = theta

    def get_pos(self):
        return (self.x, self.y)

    def get_pos_text(self):
        return "(" + "{:.0f},".format(self.x) + "{:.0f},".format(self.y) + ")" # add .2f if you want

    def as_dubin_point(self):
        return DubinPoint(self.x, self.y, self.theta)


class OwnUAV(UAV):
    def __init__(self, x, y, theta, calculated_vel=None, past_locations=[]) -> None:
        super().__init__(x, y, theta, calculated_vel, past_locations)


class TargetUAV(UAV):
    def __init__(self, x, y, theta, calculated_vel=None, past_locations=[]) -> None:
        super().__init__(x, y, theta, calculated_vel, past_locations)
        self.turnfor = 0
        self.waitfor = 0
        self.time_waited = 0
        self.since_last_pos_save = 0
