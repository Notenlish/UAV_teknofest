import xpc2
import xpc
import time


class XPlaneDataHandler:
    def __init__(self, xplane_port=50501):
        self.xp = xpc2.XPlaneUDP(defaultFreq=20)
        self.xp.FindIp()

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
        }
        self.drefs = {k: v for k, v in self.drefs_inp.items()}

        for dref, freq in self.drefs.items():
            self.xp.AddDataRef(dref, freq)

    def fetch_drefs(self):
        for k, v in self.xp.GetValues().items():
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
            "sim/flightmodel/position/psi",
        ]
        arr = [self.drefs[name] for name in datarefs]
        return {
            "P": arr[0],
            "Q": arr[1],
            "R": arr[2],
        }

    def send_data(self, data: dict[str, float | int]):
        for key, val in data.items():
            if key == "rotation":
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/phi", val[0], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/theta", val[1], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/psi", val[2], vtype="float"
                )
            elif key == "rot_acc":
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/P", val[0], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/Q", val[1], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/R", val[2], vtype="float"
                )
            elif key == "position":
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/local_x", val[0], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/local_y", val[1], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/local_z", val[2], vtype="float"
                )
            elif key == "velocity":
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/local_vx", val[0], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/local_vy", val[1], vtype="float"
                )
                self.xp.WriteDataRef(
                    "sim/flightmodel/position/local_vz", val[2], vtype="float"
                )


# Example usage
if __name__ == "__main__":
    xp_data = XPlaneDataHandler()

    # xp_data.fetch_drefs()
    # xp_data.send_data({"sim/flightmodel/position/local_y": 70})
