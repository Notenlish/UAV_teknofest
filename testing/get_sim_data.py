import socket
import struct

try:
    from utils import lat_lon_to_web_mercator
except ModuleNotFoundError:
    import sys
    from os.path import dirname, curdir

    print(__file__, curdir)
    sys.path.append(curdir)
    from utils import lat_lon_to_web_mercator

from udp_types import UDPSentenceRef, LatLongAltRef

# I just spent like 25 minutes trying to see why it was connecting but no bytes were being received
# as it turns out, clients should normally do `connect`
# and servers should normally do `bind`
# BUT for some reason
# To get UDP data from XPlane 11, you need to say BIND as an CLIENT
# WHYYYY

# chatgippity tells me that bind is to receive udp data so youre subscribing to the packets being sent
# and telling OS that you want to receive them
# while connect means that you want to send packets to a spesific addr and port, but even if we dont `connect`
# in UDP, we can still send data using sendto()


# Stream = TCP
# DGRAM = UDP


class SimCommunicator:
    def __init__(self) -> None:
        self.address = "127.0.0.1"
        self.port = 50501

        self.data = {}

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.address, self.port))
            print(f"connected to {self.address}:{self.port}")
            while True:
                raw = s.recv(41)
                print("received raw data")
                data = self.parse_udp(raw)
                self.update_values(data)

    # https://www.nuclearprojects.com/xplane/info.shtml
    # Written by chatgippity because i was lazy
    def parse_udp(self, data):
        if len(data) != 41:
            raise ValueError("Invalid UDP data length. Expected 41 bytes.")
        # Extracting the header (prolouge)
        header = data[:5]  # discard the fifth byte
        message = data[5:]

        # Parsing header components
        message_type = bytes(header[:4]).decode("utf-8")
        internal_use_byte = header[4]

        # Parsing message components
        index_number = int.from_bytes(message[:4], byteorder="little", signed=False)
        float_data = []
        for i in range(4, len(message), 4):
            float_value = struct.unpack("<f", bytes(message[i : i + 4]))[0]
            float_data.append(float_value)

        return {
            "message_type": message_type,
            "internal_use_byte": internal_use_byte,
            "index_number": index_number,
            "float_data": float_data,
        }

    def update_values(self, result: dict[str, any]):
        # {'message_type': 'DATA',
        # 'internal_use_byte': 42,
        # 'index_number': 20,
        # 'float_data': [47.463584899902344, -122.30775451660156, 403.3278503417969, 0.2671305239200592, 1.0, 403.3280029296875, 47.5, -122.0]}
        floats = result["float_data"]
        index_num = result["index_number"]
        if result["index_number"] == UDPSentenceRef.LatLongAlt.value:
            lat_deg = floats[LatLongAltRef.LAT_DEG.value]
            lon_deg = floats[LatLongAltRef.LON_DEG.value]
            alt_deg = floats[LatLongAltRef.ALT_DEG.value]
            alt_ftagl = floats[LatLongAltRef.ALT_FTAGL.value]
            is_on_runway = floats[LatLongAltRef.ON_RUNWAY.value]
            lat_origin = floats[LatLongAltRef.LAT_ORIGIN.value]
            lon_origin = floats[LatLongAltRef.LON_ORIGIN.value]
            x, y = lat_lon_to_web_mercator(lat_deg, lon_deg)
            print(x, y, lat_deg, lon_deg)


if __name__ == "__main__":
    comm = SimCommunicator()
    # fmt: off
    raw_data = [
        68, 65, 84, 65,
        60,
        18, 0, 0, 0, 171, 103, 81, 191, 187, 243, 46, 190, 103, 246, 45, 67, 156, 246, 26, 67, 47, 231, 26, 67, 0, 192, 121, 196, 0, 192, 121, 196, 85, 254, 151, 193,
    ]
    # fmt: on

    # result = comm.parse_xplane_udp_data(raw_data)
    # print(result)
    # print()
    comm.start()
