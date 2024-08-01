import cv2
import pygame
import numpy as np


class VideoException(Exception):
    pass


class VideoProcess:
    def __init__(self, config, memory, screen_area) -> None:
        self.config = config
        self.memory = memory
        self.screen_area = screen_area

        self.port = config["VIDEO_PORT"]
        self.protocol = "udp" if config["VID_USE_UDP"] else "tcp"
        self.host = config["UAV_IP"]
        self.url = f"{self.protocol}://{self.host}:{self.port}"

        if self.protocol == "tcp":
            print(
                "Please note that you need to give network access for python in firewall + open up a special inbound port for it in advanced firewall settings"
            )
            print(
                "For TCP to work the connection must already be open(first run receiver then sender)"
            )
            self.url += "/?listen"  # the client needs to specify its listening on tcp

    def _start(self, url: str):
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            raise VideoException("Cant connect(try again)")
        print("started capturing video stream.")
        while True:
            # print("ULA OKU VERI")
            ret, frame = cap.read()
            # print("ALLAHIM VERI GELIYOR")
            if not ret:
                break
            # print("ret")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, self.screen_area.size)
            frame = np.rot90(frame)
            surf = pygame.surfarray.make_surface(frame)

            self.memory["videoStream"] = surf

            # cv2.imshow('Video Stream', frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    def start(self):
        print(f"VideoReceiver Process: trying to connect to {self.url}")
        err_count = 0
        _max = 100000
        while err_count < _max:
            try:
                self._start(self.url)
            except VideoException:
                err_count += 1
            except Exception as e:
                print("err", e)
                err_count += _max
                raise Exception("aaaaaaaaaaaaaaaaaaaaa")
