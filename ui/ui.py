from random import randint
from sys import getsizeof
from threading import Event

import pygame

from utils import draw_text

from ui.earth_viewer import EarthViewer
from ui.indicator import Indicator
from ui.team_viewer import TeamViewer
from ui.command_panel import CommandPanel


pygame.font.init()


class UI:
    def __init__(
        self, config: dict[str, any], memory: dict[str, any], events: dict[str, any]
    ) -> None:
        self.screen_size = config["windowSize"]
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.UI_FPS = config["windowFPS"]
        self.is_running = False

        self.memory = memory
        self.events = events

        self.bg_col = config["windowBackground"]

        self.pixel_percent_w = self.screen_size[0] / 100
        self.pixel_percent_h = self.screen_size[1] / 100

        self.earthviewer = EarthViewer(
            config,
            self.memory,
            screen_area=pygame.Rect(
                0, 0, self.pixel_percent_w * 50, self.pixel_percent_h * 65
            ),
        )
        self.indicator = Indicator(
            config,
            screen_area=pygame.Rect(
                0,
                self.pixel_percent_h * 65,
                self.pixel_percent_w * 20,
                self.pixel_percent_h * 35,
            ),
        )
        self.teamviewer = TeamViewer(
            config,
            pygame.Rect(
                self.pixel_percent_w * 50,
                0,
                self.pixel_percent_w * 35,
                self.pixel_percent_h * 65,
            ),
        )
        self.command_panel = CommandPanel(
            config,
            pygame.Rect(
                self.pixel_percent_w * 85,
                0,
                self.pixel_percent_w * 15,
                self.pixel_percent_h * 65,
            ),
        )

        self.font = pygame.font.Font(
            config["windowFont"], size=config["windowFontSize"]
        )
        # pygame.transform.set_smoothscale_backend("SSE2")

    def start(self):
        self.dt = 1 / 1000
        self.is_running = True
        self.memory["tiles_loaded"] = {}
        while self.is_running:
            self.screen.fill(self.bg_col)

            self.earthviewer.render(self.screen, self.font)
            self.teamviewer.render(self.screen, self.font)
            draw_text(
                self.screen,
                self.font,
                f"{self.memory['i']}",
                (self.screen_size[0] * 0.5, self.screen_size[1] * 0.5),
                color="white",
            )
            self.indicator.render(self.screen)
            self.command_panel.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        self.earthviewer.change_zoom(1)
                    if event.key == pygame.K_F2:
                        self.earthviewer.change_zoom(-1)
                if event.type == pygame.QUIT:
                    self.is_running = False
                    self.events["close_app"].set()
                    break

            events = pygame.key.get_pressed()
            if events[pygame.K_w]:
                self.earthviewer.move(0, -1, self.dt)
            if events[pygame.K_a]:
                self.earthviewer.move(-1, 0, self.dt)
            if events[pygame.K_s]:
                self.earthviewer.move(0, 1, self.dt)
            if events[pygame.K_d]:
                self.earthviewer.move(1, 0, self.dt)

            self.dt = self.clock.tick(self.UI_FPS) / 1000
            pygame.display.update()
