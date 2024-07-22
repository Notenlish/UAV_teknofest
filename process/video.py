import cv2
import pygame
import numpy as np
import os
import socket


class VideoException(Exception):
    pass


class VideoProcess:
    def __init__(self, config, memory, screen_area) -> None:
        self.config = config
        self.memory = memory
        self.screen_area = screen_area

        self.port = config["videoPort"]
        self.protocol = "udp" if config["sendVideoUDP"] else "tcp"
        self.host = config["videoHost"]
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
        print(f"attempting to connect {url}")
        cap = cv2.VideoCapture(url)
        print("started capture")
        if not cap.isOpened():
            raise VideoException("Cant connect(try again)")

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
        print("starting capture")
        err_count = 0
        while err_count < 100000:
            try:
                self._start(self.url)
            except VideoException:
                err_count += 1
            except Exception as e:
                print("err", e)
                err_count += 10
                raise Exception("aaaaaaaaaaaaaaaaaaaaa")
