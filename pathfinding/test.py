import pygame

import visualizer


class App:
    def __init__(self) -> None:
        self.window = pygame.display.set_mode((500, 500))
        self.clock = pygame.time.Clock()
        self.max_fps = 60
        self.visualizer = visualizer.Visualizer(self.window)
    
    def run(self):
        while True:
            self.visualizer.draw([])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
            self.window.fill("#EBEBEB")
            pygame.display.update()
            self.clock.tick(self.max_fps)
            
if __name__ == '__main__':
    app = App()
    app.run()