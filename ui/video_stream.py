import pygame

class VideoStream:
    def __init__(self, config, memory, rect) -> None:
        self.config = config
        self.memory = memory
        self.screen_area = rect

    def render(self, screen):
        stream = self.memory["videoStream"]
        if stream:
            screen.blit(stream, (self.screen_area.topleft))
        else:
            pygame.draw.rect(screen, "red", self.screen_area, width=4)