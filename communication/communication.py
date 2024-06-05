from threading import Event
from pymavlink import mavutil, mavparm
import time


class Communication:
    def __init__(self) -> None:
        pass

    def start(self, MEMORY: dict[str, any], EVENTS: dict[str, Event]) -> None:
        # Start a connection listening on a UDP port
        # com7 for windows
        # /dev/ttyUSB0 for linux
        the_connection: mavutil.mavserial = mavutil.mavlink_connection(
            "com7", baud=57600
        )

        # Wait for the first heartbeat
        #   This sets the system and component ID of remote system for the link

        the_connection.wait_heartbeat()
        
        print(
            "Heartbeat from system (system %u component %u)"
            % (the_connection.target_system, the_connection.target_component)
        )


if __name__ == "__main__":
    comm = Communication()
    comm.start({}, {})
