import socket
import threading

import utils

HOST, PORT = utils.read_json("config.json")


class ThreadedTCPClient():
    def __init__(self) -> None:
        self.HOST, self.PORT = utils.read_json("config.json")
        self.socket = socket.socket()
        self.msg_queue = ["MSG 1", "MSG 2"]

    def add_msg_to_queue(self, msg: str):
        self.msg_queue.append(msg)

    def run(self):
        self.thread = threading.Thread(target=self.thread_run)
        self.thread.start()

    def thread_run(self):
        def close_connection(self):
            self.socket.close()

        def connect(self):
            self.socket.connect((self.HOST, self.PORT))
        
        def receive_message(self):
            data = self.socket.recv(1024)
            if data == b"NOTHING_TO_SEND":
                if len(self.msg_queue) == 0:
                    pass
                else:
                    pass
            print(f"Received from server: {data.decode()}")
        
        try:
            connect(self)
            while True:
                try:
                    msg_to_send = self.msg_queue.pop(0).upper().encode()
                    if msg_to_send == b'EXIT':
                        break
                    self.socket.sendall(msg_to_send)  # send msg
                    print(f"Sent message to server: {msg_to_send}")
                except IndexError:
                    pass
                receive_message(self)
        finally:
            print("closing connection")
            close_connection(self)      


if __name__ == "__main__":
    try:
        client = ThreadedTCPClient()
        client.run()
    except Exception as e:
        client.thread.join()
        print(e)
    