import xpc2
import xpc


class XPlaneDataHandler:
    def __init__(self, xplane_port=50501):
        self.client = xpc2.XPlaneUDP(port=xplane_port)

        # None = default frequency
        self.drefs = {
            "sim/flightmodel/position/local_x": None,
            "sim/flightmodel/position/local_y": None,
            "sim/flightmodel/position/local_z": None,
            "sim/flightmodel/position/local_vx": None,
            "sim/flightmodel/position/local_vy": None,
            "sim/flightmodel/position/local_vz": None,
            "sim/flightmodel/position/P":None,  # roll
            "sim/flightmodel/position/Q":None,  # pitch
            "sim/flightmodel/position/R":None,  # yaw
        }

        for dref, freq in self.drefs.items():
            self.client.AddDataRef(dref, freq)

    def get_drefs(self, drefs: list[str]):
        vals = []
        for name in drefs:
            val = self.client.getDREF(name)
            vals.append(val)
        return vals

    def get_position(self):
        """Retrieve the current position (local_x, local_y, local_z) of the aircraft."""
        datarefs = [
            "sim/flightmodel/position/local_x",
            "sim/flightmodel/position/local_y",
            "sim/flightmodel/position/local_z",
        ]
        position = self.get_drefs(datarefs)
        return {
            "local_x": position[0][0],
            "local_y": position[1][0],
            "local_z": position[2][0],
        }

    def get_velocity(self):
        """Retrieve the current velocity (local_vx, local_vy, local_vz) of the aircraft."""
        datarefs = [
            "sim/flightmodel/position/local_vx",
            "sim/flightmodel/position/local_vy",
            "sim/flightmodel/position/local_vz",
        ]
        velocity = self.get_drefs(datarefs)
        return {
            "local_vx": velocity[0][0],
            "local_vy": velocity[1][0],
            "local_vz": velocity[2][0],
        }

    def get_orientation(self):
        """Retrieve the current orientation (pitch, roll, yaw) of the aircraft."""
        datarefs = [
            "sim/flightmodel/position/P",
            "sim/flightmodel/position/Q",
            "sim/flightmodel/position/R",
        ]
        orientation = self.client.getDREFs(datarefs)
        return {
            "pitch": orientation[0][0],
            "roll": orientation[1][0],
            "yaw": orientation[2][0],
        }

    def get_all_data(self):
        """Retrieve all required data in a single call."""
        print(self.client.getDREF("sim/flightmodel/position/P"))
        # position = self.get_position()
        # velocity = self.get_velocity()
        # orientation = self.get_orientation()
        return {
            # "position": position,
            # "velocity": velocity,
            # "orientation": orientation
        }

    def send_data(self, data):
        """
        Send data to X-Plane.
        This method can be customized to send commands or control inputs to the simulator.
        """
        # Example: Set the aircraft position
        if "position" in data:
            self.client.sendPOSI(data["position"])

        # Example: Set the aircraft velocity (Note: not directly supported by X-Plane Connect)
        if "velocity" in data:
            print("I'm not setting velocity")
            pass  # Handle velocity setting if needed

        # Example: Set the aircraft orientation
        if "orientation" in data:
            self.client.sendCTRL(data["orientation"])


# Example usage
if __name__ == "__main__":
    xplane_data_handler = XPlaneDataHandler()
    position = xplane_data_handler.get_position()
    velocity = xplane_data_handler.get_velocity()
    orientation = xplane_data_handler.get_orientation()

    print("Position:", position)
    print("Velocity:", velocity)
    print("Orientation:", orientation)

    # Example of sending data
    data_to_send = {
        "position": [0, 10, 0, 0, 0, 0],  # Example position data
        "orientation": [0, 0, 0, 0],  # Example orientation data
    }
    xplane_data_handler.send_data(data_to_send)
