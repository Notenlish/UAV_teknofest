import pygame
from camera import Camera
from kalman import ThetaKalmanFilter, VelocityKalmanFilter
from path_finding import PathFinding
from telemetry import Telemetry
from uav import OwnUAV, TargetUAV
from visualizer import Visualizer
from predictor import Predictor


# TODO: predictor should also predict own uav pos
# or maybe not? Since we can run the telemetry multiple times a second while the targetuav is only updated once per second
# and it would make it difficult for the whole structure
# I should probably take the lazy approach.


# FIXME: We draw measured ones first and then the predicted ones, which hides the past loc points of measured ones
# I should stop cloning the entire objects and make sure that the old past loc arr of predicted objects are not replaced by the ones of measured obj
# measured ların past location ları predicted nesnelerinin üzerine replace ediyor nesneleri direkten deepcopy yaptığımdan


class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((700, 500))
        pygame.display.set_caption("Pathfinding")
        self.clock = pygame.time.Clock()

        # config
        self.max_fps = 60
        self.step_size = 20
        self.turning_radius = 50

        self.own_uav = OwnUAV(100, 100, theta=0, vel=50)
        self.target_uav = TargetUAV(400, 300, theta=0, vel=50)

        self.camera = Camera()
        self.visualizer = Visualizer(self.window, self.camera, pygame.display)
        self.telemetry = Telemetry(self.own_uav, self.target_uav)
        self.path_finding = PathFinding(
            self.own_uav.as_dubin_point(),
            self.target_uav.as_dubin_point(),
            self.turning_radius,
            self.step_size,
        )
        self.theta_kalman = ThetaKalmanFilter(
            initial_theta=self.target_uav.theta, theta_rate_of_change=0
        )
        self.vel_kalman = VelocityKalmanFilter(
            initial_vel=self.target_uav.vel, acceleration=0
        )
        self.predictor = Predictor(
            self.theta_kalman, self.vel_kalman, self.path_finding
        )

        self.telemetry.init(self.path_finding, self.predictor)
        self.visualizer.init(self.path_finding)

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

            self.input(dt)
            result = self.path_finding.run()

            self.visualizer.draw(*result)


if __name__ == "__main__":
    app = App()
    app.run()
