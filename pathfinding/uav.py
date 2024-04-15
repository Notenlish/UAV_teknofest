from shape import DubinPoint

class UAV:
    def __init__(self, x, y, theta, calculated_vel=None, past_locations=[]) -> None:
        self.x = x
        self.y = y
        self.calculated_vel = calculated_vel
        self.past_locations = past_locations
        self.theta = theta
    
    def get_pos(self):
        return (self.x, self.y)
    
    def as_dubin_point(self):
        return DubinPoint(self.x, self.y, self.theta)


class OwnUAV(UAV):
    def __init__(self, x, y, theta, calculated_vel=None, past_locations=[]) -> None:
        super().__init__(x, y, theta, calculated_vel, past_locations)


class TargetUAV(UAV):
    def __init__(self, x, y, theta, calculated_vel=None, past_locations=[]) -> None:
        super().__init__(x, y, theta, calculated_vel, past_locations)

