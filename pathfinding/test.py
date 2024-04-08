import pygame

from shape import DubinPoint

from visualizer import Visualizer
from path_maker import PathMaker


class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.visualizer = Visualizer(self.window)
        self.pathmaker = PathMaker()
        self.turning_radius = 50.0
        self.step_size = 20

        self.result_path, self.sample_results = self.pathmaker.run(
            DubinPoint(50, 380, 1),
            DubinPoint(450, 90, 0.5),
            rho=self.turning_radius,
            step_size=self.step_size,
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
            self.visualizer.draw(self.result_path, self.sample_results)
            pygame.display.update()
            self.clock.tick(self.max_fps)


if __name__ == "__main__":
    app = App()
    app.run()
