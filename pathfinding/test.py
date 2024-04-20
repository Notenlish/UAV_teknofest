import pygame

from shape import DubinPoint

from visualizer import Visualizer
from pathfinder import Pathfinder
from telemetry import Telemetry
from kalman import UAVKalmanFilter
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
        self.telemetry = Telemetry()
        self.pathfinding = Pathfinder(
            self.telemetry.own_uav.as_dubin_point(),
            self.telemetry.target_uav.as_dubin_point(),
            self.turning_radius, self.step_size )
        self.kalman = UAVKalmanFilter(
            target_dub_pos=self.pathfinding.target_uav_dub_pos,
            measurement_noise_variance=0.1, process_noise_variance=0.01)

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


    # kodu temizle
    # kalman alakalı her şeyi yok et
    # yeni bir uavkalmanfilter classı yaz
    # ama sadece thetayı tahmin etmeye çalışacak
    # theta 0-2 arasında mı olmalı yoksa istediği herhangi bir değer olabilir mi bilmiyorum

    def run(self):
        while True:
            dt = self.clock.tick(self.max_fps)  # ms
            data = self.telemetry.run(dt)
            if data:
                self.pathfinding.own_uav_past_locations.append(self.pathfinding.own_uav_dub_pos)
                self.pathfinding.target_uav_past_locations.append(self.pathfinding.target_uav_dub_pos)
                self.pathfinding.own_uav_dub_pos = data["own_uav"]
                self.pathfinding.target_uav_dub_pos = data["target_uav"]
                # self.kalman.update_state_transition_matrix(dt=1, velocity=self.telemetry.uav_vel)
                predict = self.kalman.predict()
                updated_state = self.kalman.update(self.pathfinding.target_uav_dub_pos)
                self.pathfinding.predicted = DubinPoint.from_array(predict)
                self.pathfinding.updated = DubinPoint.from_array(updated_state)

            predict = self.kalman.predict()
            self.pathfinding.predicted = DubinPoint.from_array(predict)

            results = self.pathfinding.run()
            self.input(dt)

            self.visualizer.draw(*results.values())


if __name__ == "__main__":
    app = App()
    app.run()
