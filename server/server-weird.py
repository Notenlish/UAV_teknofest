import socketserver
import threading

import utils

# TODO: automate data sending & commands


HOST, JSON = utils.read_json("config.json")


class SimpleSocketHandler(socketserver.BaseRequestHandler):
    def handle(self):  # override handle method
        while True:
            data = self.request.recv(1024)
            if not data:
                print("breaking")
                break
            print(f"Message from Client: {data}")

            try:
                # print("Getting messages to send")
                msg_to_send = self.msg_queue.pop(0).encode()
                self.request.sendall(msg_to_send)
                print(f"sending message: {msg_to_send}")
            except IndexError:
                self.request.sendall(b"NOTHING_TO_SEND")
                print("No messages left to send :(")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(
        self,
        server_address,
        RequestHandlerClass,
        bind_and_activate: bool = True,
        msg_queue_ref=[],
    ) -> None:
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)
        # I legit don't know how to structure stuff related to threading and/or sockets
        # this is worse than yanderedev's code :skull
        self.RequestHandlerClass.msg_queue = (
            msg_queue_ref  # pass msq_queue to sockethandler
        )


class ThreadedTCPServerManager:
    def __init__(self) -> None:
        self.thread = threading.Thread(target=self.thread_init_and_run)
        self.msg_queue = []

    def add_msg_to_queue(self, msg):
        self.msg_queue.append(msg)

    def thread_init_and_run(self):
        server_thread = ThreadedTCPServer(
            (HOST, PORT), SimpleSocketHandler, msg_queue_ref=self.msg_queue
        )
        print(f"Server running on {HOST}:{PORT}")

        try:
            server_thread.serve_forever()
            print("asdsa")
            # server_thread.join()
        except KeyboardInterrupt:
            print("Server shutting down.")
            server_thread.shutdown()  # I should move this OUTSIDE of the loop
            server_thread.server_close()


if __name__ == "__main__":
    HOST, PORT = utils.read_json("config.json")

    # host : The server's hostname or IP address
    # Port : The port used by the server # between 1 and 65k
    # NOTE: sockets from 0 to 1023 are reserved

    try:
        manager = ThreadedTCPServerManager()
        manager.thread_init_and_run()
    except Exception as e:
        manager.thread.join()
        print(manager.thread.is_alive())
        print(e)
