
from uav import OwnUAV, TargetUAV

from random import random

# TODO simulate data arriving late
# TODO more than 1 target uav data being given by telemetry

class Telemetry:
    def __init__(self, own_uav: OwnUAV, target_uav: TargetUAV) -> None:
        self.own_uav = own_uav
        self.target_uav = target_uav
        self.time_passed = 0
    
    def run(self, dt):
        self.time_passed += dt / 1000

        if self.time_passed >= 1 + (1*random()) : # s
            print(f"More than {self.time_passed} seconds have passed")
            self.time_passed = 0
            self.target_uav.x += 25 * random()