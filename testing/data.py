import xpc2
from xpc import XPlaneConnect
import struct


class XPlaneDataHandler:
    def __init__(self, xplane_port=50501):
        self.xp_udp = xpc2.XPlaneUDP(defaultFreq=10)
        self.xp_udp.FindIp()

        # None = default frequency
        self.drefs_inp = {
            "sim/flightmodel/position/local_x": None,
            "sim/flightmodel/position/local_y": None,
            "sim/flightmodel/position/local_z": None,
            "sim/flightmodel/position/local_vx": None,
            "sim/flightmodel/position/local_vy": None,
            "sim/flightmodel/position/local_vz": None,
            "sim/flightmodel/position/phi": None,  # roll
            "sim/flightmodel/position/theta": None,  # pitch
            "sim/flightmodel/position/psi": None,  # yaw
            "sim/multiplayer/position/plane1_phi": None,
            "sim/multiplayer/position/plane1_theta": None,
            "sim/multiplayer/position/plane1_psi": None,
            "sim/multiplayer/position/plane1_x": None,
            "sim/multiplayer/position/plane1_y": None,
            "sim/multiplayer/position/plane1_z": None,
            "sim/multiplayer/position/plane2_phi": None,
            "sim/multiplayer/position/plane2_theta": None,
            "sim/multiplayer/position/plane2_psi": None,
            "sim/multiplayer/position/plane2_x": None,
            "sim/multiplayer/position/plane2_y": None,
            "sim/multiplayer/position/plane2_z": None,
            "sim/operation/override/override_planepath": None,
        }
        self.drefs = {k: v for k, v in self.drefs_inp.items()}

        for dref, freq in self.drefs.items():
            self.xp_udp.AddDataRef(dref, freq)

    def fetch_drefs(self):
        for k, v in self.xp_udp.GetValues().items():
            self.drefs[k] = v

    def get_position(self):
        """(local_x, local_y, local_z) of the aircraft."""
        datarefs = [
            "sim/flightmodel/position/local_x",
            "sim/flightmodel/position/local_y",
            "sim/flightmodel/position/local_z",
        ]
        arr = [self.drefs[name] for name in datarefs]
        return {
            "local_x": arr[0],
            "local_y": arr[1],
            "local_z": arr[2],
        }

    def get_velocity(self):
        """(local_vx, local_vy, local_vz) of the aircraft."""
        datarefs = [
            "sim/flightmodel/position/local_vx",
            "sim/flightmodel/position/local_vy",
            "sim/flightmodel/position/local_vz",
        ]
        arr = [self.drefs[name] for name in datarefs]
        return {
            "local_vx": arr[0],
            "local_vy": arr[1],
            "local_vz": arr[2],
        }

    def get_rotation(self):
        """(pitch, roll, yaw) of the aircraft."""
        datarefs = [
            "sim/flightmodel/position/phi",
            "sim/flightmodel/position/theta",
            "sim/flightmodel/position/psi",  # yaw
        ]
        arr = [self.drefs[name] for name in datarefs]
        return arr

    def get_ai_rotation(self):
        datarefs = [
            "sim/multiplayer/position/plane1_phi",
            "sim/multiplayer/position/plane1_theta",
            "sim/multiplayer/position/plane1_psi",
        ]
        arr = [self.drefs[name] for name in datarefs]
        return arr

    def get_ai_position(self):
        datarefs = [
            "sim/multiplayer/position/plane1_x",
            "sim/multiplayer/position/plane1_y",
            "sim/multiplayer/position/plane1_z",
        ]
        arr = [self.drefs[name] for name in datarefs]
        return arr

    def set_sim_running(self, values: list[bool, 20]):
        dref = "sim/operation/override/override_planepath"
        self.xp_udp.WriteDataRef()

    def send_data(self, data: dict[str, list[float | int]]):
        for key, val in data.items():
            if key == "rotation":
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/phi", val[0], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/theta", val[1], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/psi", val[2], vtype="float"
                )
            elif key == "rot_acc":
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/P", val[0], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/Q", val[1], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/R", val[2], vtype="float"
                )
            elif key == "position":
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/local_x", val[0], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/local_y", val[1], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/local_z", val[2], vtype="float"
                )
            elif key == "velocity":
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/local_vx", val[0], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/local_vy", val[1], vtype="float"
                )
                self.xp_udp.WriteDataRef(
                    "sim/flightmodel/position/local_vz", val[2], vtype="float"
                )
            elif key == "ai_position":
                self.sendPOSI()


# Example usage
if __name__ == "__main__":
    xp_data = XPlaneDataHandler()

    # xp_data.fetch_drefs()
    # xp_data.send_data({"sim/flightmodel/position/local_y": 70})
