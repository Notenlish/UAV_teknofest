import socket

import utils

global msg_queue
msg_queue = []

HOST, PORT  = utils.read_json("config.json")


class TCPServer:
    def __init__(self) -> None:
        pass
    
    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.bind((HOST, PORT))

        # (max 2 connections in the queue)
        self.server_socket.listen()
        print(f"Server listening on {HOST} : {PORT}")
        
        # Normally you'd use while True: to wait for a bunch of connections but we only have 1
        
        client_socket, client_address = self.server_socket.accept()
        print(f"Connection established with {client_address}")

        client_socket.sendall("WELCOME".encode())
        while True:
            data = client_socket.recv(1024).decode().upper()
            if not data: # empty
                client_socket.close()
                break
            print(f"Received data: {data}")

            if data == "STOP":
                client_socket.close()
                break


if __name__ == '__main__':
    # KeyboardInterrupt event listener çalışmıyor çünkü socket ların çalışma prensibi
    # nedeniyle socket in aktif olarak mesaj beklediği veya gönderdiği sırada fln 
    # event şeysi çalışmıyor
    # tek çözüm ayrı thread a taşımak
    # ve bunu düzgün yapmak
    try:
        server = TCPServer()
        server.start()
    except KeyboardInterrupt:
        pass
