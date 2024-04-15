import pygame

from shape import DubinPoint

from visualizer import Visualizer
from pathfinder import Pathfinder
from telemetry import Telemetry


class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        
        # config
        self.max_fps = 60
        self.step_size = 20
        self.turning_radius = 50

        self.visualizer = Visualizer(self.window, pygame.display)
        self.pathfinding = Pathfinder(self.turning_radius, self.step_size)
        self.telemetry = Telemetry(self.pathfinding.own_uav, self.pathfinding.target_uav)
        # uav classes prob shouldnt be in pathfinding but whatever

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                raise SystemExit

    def run(self):
        while True:
            dt = self.clock.tick(self.max_fps)  # ms
            data = self.telemetry.run(dt)
            
            results = self.pathfinding.run(data={})
            self.input()
            
            self.visualizer.draw(*results.values())
            


if __name__ == "__main__":
    app = App()
    app.run()
