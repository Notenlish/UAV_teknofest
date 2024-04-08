import pygame

from shape import Point

class Visualizer:
    def __init__(self, surface: pygame.Surface) -> None:
        self.surface = surface
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 16)

    def draw_text(self, text, point: Point):
        surf = self.font.render(text)
        self.surface.blit(surf, point.get_tuple())

    def draw(self, path: list[Point]):
        self.surface.fill("#E6E6E6")
        if path:
            pygame.draw.lines(self.surface, "black", False, path)
        
        
        

