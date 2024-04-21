import pygame
from camera import Camera
from kalman import UAVKalmanFilter
from pathfinder import PathFinding
from shape import DubinPoint
from telemetry import Telemetry
from uav import OwnUAV, TargetUAV
from visualizer import Visualizer


class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Test")
        self.clock = pygame.time.Clock()

        # config
        self.max_fps = 60
        self.step_size = 20
        self.turning_radius = 50

        self.own_uav = OwnUAV(100, 100, theta=0)
        self.target_uav = TargetUAV(400, 300, theta=0)

        self.camera = Camera()
        self.visualizer = Visualizer(self.window, self.camera, pygame.display)
        self.telemetry = Telemetry(self.own_uav, self.target_uav)
        self.path_finding = PathFinding(
            self.own_uav.as_dubin_point(),
            self.target_uav.as_dubin_point(),
            self.turning_radius,
            self.step_size,
        )
        self.kalman = UAVKalmanFilter(
            target_dub_pos=self.path_finding.target_uav_dub_pos,
            measurement_noise_variance=0.1,
            process_noise_variance=0.01,
        )

        self.telemetry.init(self.path_finding)

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

        self.telemetry.set_own_uav_theta(self.camera.get_pos(), pygame.mouse.get_pos())

    # kodu temizle
    # kalman alakalı her şeyi yok et
    # yeni bir uavkalmanfilter classı yaz
    # ama sadece thetayı tahmin etmeye çalışacak
    # theta 0-2 arasında mı olmalı yoksa istediği herhangi bir değer olabilir mi bilmiyorum

    def run(self):
        while True:
            dt = self.clock.tick(self.max_fps)  # ms
            self.telemetry.run(dt)

            # self.kalman.update_state_transition_matrix(dt=1, velocity=self.telemetry.uav_vel)
            # predict = self.kalman.predict()
            # updated_state = self.kalman.update(self.pathfinding.target_uav_dub_pos)
            # self.pathfinding.predicted = DubinPoint.from_array(predict)
            # self.pathfinding.updated = DubinPoint.from_array(updated_state)

            # predict = self.kalman.predict()
            # self.pathfinding.predicted = DubinPoint.from_array(predict)

            results = self.path_finding.run()
            self.input(dt)

            self.visualizer.draw(*results.values())


if __name__ == "__main__":
    app = App()
    app.run()
