import pygame

from shape import DubinPoint

from visualizer import Visualizer
from pathfinder import Pathfinder
from telemetry import Telemetry
from camera import Camera
import math


class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Test")
        self.clock = pygame.time.Clock()

        # config
        self.max_fps = 60
        self.step_size = 20
        self.turning_radius = 50

        self.camera = Camera()
        self.visualizer = Visualizer(self.window, self.camera, pygame.display)
        self.pathfinding = Pathfinder(self.turning_radius, self.step_size)
        self.telemetry = Telemetry(
            self.pathfinding.own_uav, self.pathfinding.target_uav
        )
        # uav classes prob shouldnt be in pathfinding but whatever

    def input(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera.move(0, -1, dt)
        if keys[pygame.K_a]:
            self.camera.move(-1, 0, dt)
        if keys[pygame.K_s]:
            self.camera.move(0, 1, dt)
        if keys[pygame.K_d]:
            self.camera.move(1, 0, dt)

        campos = self.camera.get_pos()
        mousepos = pygame.mouse.get_pos()
        pos = (mousepos[0] + campos[0], mousepos[1] + campos[1])
        diffx = pos[0] - self.telemetry.own_uav.x
        diffy = pos[1] - self.telemetry.own_uav.y

        theta = math.atan2(diffy, diffx)
        self.telemetry.own_uav.theta = theta

    def run(self):
        while True:
            dt = self.clock.tick(self.max_fps)  # ms
            data = self.telemetry.run(dt)

            results = self.pathfinding.run(data={})
            self.input(dt)

            self.visualizer.draw(*results.values())


if __name__ == "__main__":
    app = App()
    app.run()
