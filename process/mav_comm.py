import socket


class MavComm:
    def __init__(self, app, config, memory) -> None:
        self.app = app
        self.memory = memory
        HOST = "127.0.0.1"
        PORT = config["MAVLINK_PORT"]
        self.addr = (HOST, PORT)

    def start(self):
        print(f"MAV Communications çalışıyor {self.addr}")
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(self.addr)
            print("MAVlink mesajları dinleniyor.")
            # while True:
            #    print("okuy")
            #    sock.sendall(b"31")
            #    data, addr = sock.recvfrom(280)
            #
            #
            # print(data, addr)
