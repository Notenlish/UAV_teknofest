import socket
import struct

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


def get_xp11_data(address="127.0.0.1", port=50501):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((address, port))
                print(f"connected to {address}:{port}")

                while True:
                    raw = s.recv(41)
                    print("received raw data")
                    data = parse_xplane_udp_data(raw)
                    print(data)
        except ConnectionRefusedError:
            print("error, trying again")
            continue
        except TimeoutError:
            print("timeout yedim lan")
            continue


# https://www.nuclearprojects.com/xplane/info.shtml
# Written by chatgippity because i was lazy
def parse_xplane_udp_data(data):
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


if __name__ == "__main__":
    # fmt: off
    raw_data = [
        68, 65, 84, 65,
        60,
        18, 0, 0, 0, 171, 103, 81, 191, 187, 243, 46, 190, 103, 246, 45, 67, 156, 246, 26, 67, 47, 231, 26, 67, 0, 192, 121, 196, 0, 192, 121, 196, 85, 254, 151, 193,
    ]
    # fmt: on
    result = parse_xplane_udp_data(raw_data)
    print(result)
    print()
    get_xp11_data()
