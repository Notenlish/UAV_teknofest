import pygame
from threading import Event

from functools import lru_cache

pygame.font.init()


class UI:
    def __init__(self, config: dict[str, any]) -> None:
        self.screen_size = config["windowSize"]
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.UI_FPS = config["windowFps"]
        self.is_running = False

        self.earth = pygame.image.load("ui/earth.jpg").convert()

        self.font = pygame.font.Font("ui/Renogare-Regular.otf", size=20)

    def _position_anchor(
        self, rect: pygame.Rect | pygame.FRect, anchor: tuple[str, str]
    ):
        resulty = None
        resultx = None
        if anchor[0] == "left":
            resultx = rect.left
        if anchor[0] == "center":
            resultx = -rect.centerx
        if anchor[0] == "right":
            resultx = -rect.right

        if anchor[1] == "top":
            resulty = rect.top
        if anchor[1] == "center":
            resulty = -rect.centery
        if anchor[1] == "bottom":
            resulty = rect.bottom

        return (resultx, resulty)

    @lru_cache(maxsize=None)
    def _draw_earth(self, zoom):
        # earth will occupy 60% of screen width and 60% of height
        # if zoom = 1 --> get the entire earth and attempt to draw it on the screen
        # if zoom = 2 --> get half of the earth and draw it on the screen
        earth_rect = self.earth.get_rect()
        earth_screen_area = pygame.Rect(0,0, self.screen_size[0] * 60 / 100, self.screen_size[1] * 60 / 100)
        crop_area = pygame.Rect(0, 0, earth_rect.width / zoom, earth_rect.height / zoom)
        cropped = self.earth.subsurface(crop_area)
        scaled = pygame.transform.scale(cropped, earth_screen_area.size)
        self.screen.blit(cropped, (0,0), scaled)

    def _draw_text(
        self,
        text,
        point: tuple[float, float],
        color="black",
        anchor: tuple[str, str] = ("center", "center"),
    ):
        surf = self.font.render(text, antialias=True, color=color)
        rect = surf.get_rect()
        anchor = self._position_anchor(rect, anchor)
        anchor = (anchor[0] + point[0], anchor[1] + point[1])
        self.screen.blit(surf, anchor)

    def start(self, MEMORY: dict[str, any], EVENTS: dict[str, Event]):
        self.is_running = True
        zoom = 1
        while self.is_running:
            self.screen.fill("white")

            self._draw_text(
                f"{MEMORY["i"]}", (self.screen_size[0] * 0.5, self.screen_size[1] * 0.5)
            )
            self._draw_earth(zoom)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    pass
                if event.type == pygame.QUIT:
                    self.is_running = False
                    EVENTS["close_app"].set()
                    break

            self.dt = self.clock.tick(self.UI_FPS)
            pygame.display.update()
