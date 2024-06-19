import socket

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


def get_xp11_data(address="127.0.0.1", port=50501):
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.bind((address, port))
                print(f"connected to {address}:{port}")

                while True:
                    data = s.recv(1024)
                    print("received data")
                    print(data)
        except ConnectionRefusedError:
            print("error, trying again")
            continue
        except TimeoutError:
            print("timeout yedim lan")
            continue


if __name__ == "__main__":
    get_xp11_data()