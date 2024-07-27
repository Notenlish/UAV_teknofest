from data import XPlaneDataHandler
from xpc2 import XPlaneTimeout
import math
import numpy as np


class Testing:
    def __init__(self) -> None:
        self.xplane = XPlaneDataHandler()

    def run(self):
        self.xplane.fetch_drefs()

        # start_pos = {"latitude": 41.015137, "longtitude": 28.979530, "altitude": 100}
        # self.xplane.sendPOSI(**start_pos, ac=0)
        # self.xplane.send_data({"position": start_pos})
        self.rot = self.xplane.get_rotation()

        yaw = self.rot[2]
        yaw_rad = math.radians(yaw)
        length = 1

        xyz_inc = np.array([math.sin(yaw_rad) * length, 0, math.cos(yaw_rad) * length])
        # ai_pos = start_pos  # + xyz_inc
        # self.xplane.send_data({"ai_position": ai_pos})

        self.xplane.fetch_drefs()
        while True:
            self.xplane.fetch_drefs()

            self.rot = np.array(self.xplane.get_rotation())
            self.ai_rot = np.array(self.xplane.get_ai_rotation())

            self.xplane.xp_udp.WriteDataRef(
                "sim/operation/override/override_planepath", [False for _ in range(20)]
            )
            # self.rotate_to(np.array([0, 0, 300]))
            # self.xplane.sendPOSI(**start_pos, ac=0)

    def rotate_to(self, wanted_rot: np.ndarray | list):
        if type(wanted_rot) == list:
            wanted_rot = np.array(wanted_rot)
        dif = wanted_rot - self.rot
        # print(wanted_rot, self.rot)
        self.xplane.send_data({"rot_acc": dif})


if __name__ == "__main__":
    testing = Testing()
    try:
        testing.run()
    except KeyboardInterrupt:
        raise SystemExit
    except XPlaneTimeout:
        print("most likely a keyboard interrupt")
