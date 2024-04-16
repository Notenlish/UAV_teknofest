
from uav import OwnUAV, TargetUAV

from random import random
import math

# TODO simulate data arriving late
# TODO more than 1 target uav data being given by telemetry

class Telemetry:
    def __init__(self, own_uav: OwnUAV, target_uav: TargetUAV) -> None:
        self.own_uav = own_uav
        self.target_uav = target_uav
        self.time_passed = 0
    
    def run(self, dt):
        self.time_passed += dt / 1000

        if self.time_passed >= 0.3 + (0.3*random()) : # s
            print(f"More than {self.time_passed} seconds have passed")
            self.time_passed = 0
            self.target_uav.past_locations.append(self.target_uav.get_pos())
            random_theta = random() * 4
            self.target_uav.x += math.cos(random_theta) * 10
            self.target_uav.y += math.sin(random_theta) * 10
            self.target_uav.theta = random_theta