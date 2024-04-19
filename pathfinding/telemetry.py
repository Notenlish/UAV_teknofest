from uav import OwnUAV, TargetUAV

from random import random, choice
import math

# TODO simulate data arriving late
# TODO more than 1 target uav data being given by telemetry


class Telemetry:
    def __init__(self, own_uav: OwnUAV, target_uav: TargetUAV) -> None:
        self.own_uav = own_uav
        self.target_uav = target_uav

    def target_change(self):
        target_uav = self.target_uav
        if target_uav.time_waited >= target_uav.waitfor:  # seconds
            print(f"{target_uav.waitfor:.2f} seconds passed")
            self.time_passed = 0

            _rot_dir = choice([-1, 1])
            target_uav.turnfor = ((random() * 0.7) + 0.05) * _rot_dir

            target_uav.waitfor = (random() * 2) + 2
            target_uav.time_waited = 0
            target_uav.since_last_pos_save = 0

    def run(self, dt):
        target_uav = self.target_uav
        own_uav = self.own_uav

        time_passed_s = dt / 1000
        target_uav.time_waited += time_passed_s

        dist_x = target_uav.x - own_uav.x
        dist_y = target_uav.y - own_uav.y
        if math.sqrt(dist_x**2 + dist_y**2) > 400:
            own_uav.x += dist_x * 0.1 * time_passed_s
            own_uav.y += dist_y * 0.1 * time_passed_s

        self.target_change()

        if target_uav.since_last_pos_save <= 0:
            target_uav.past_locations.append(target_uav.get_pos())
            target_uav.since_last_pos_save = 0.5

        target_uav.theta += target_uav.turnfor * time_passed_s
        target_uav.theta += target_uav.turnfor * time_passed_s
        target_uav.x += math.cos(target_uav.theta) * 50 * time_passed_s
        target_uav.y += math.sin(target_uav.theta) * 50 * time_passed_s
        target_uav.since_last_pos_save -= time_passed_s
