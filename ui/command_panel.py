from math import sin, cos
import os

import pygame


class CommandPanel:
    def __init__(self, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.screen_area = screen_area

        self.icon_size = (64, 64)

        self.bg_col = config["windowBackground"]

        self.commands = config["windowCommands"]
        self._load_images()

    def _load_images(self):
        for i, item in enumerate(self.commands):
            path: str = item["imagePath"]
            if path.endswith("png") or path.endswith("jpg") or path.endswith("jpeg"):
                image = pygame.image.load(path)
            elif path.endswith("svg"):
                image = pygame.image.load_sized_svg(path, self.icon_size)
            else:
                image = pygame.transform.scale(
                    pygame.image.load("ui/data/empty.png"), self.icon_size
                )
            self.commands[i]["image"] = image

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.bg_col, self.screen_area)

        pos = [self.screen_area.centerx - (self.icon_size[0] // 2), 10]
        for item in self.commands:
            screen.blit(item["image"], pos)
            pos[1] += 10 + item["image"].get_size()[1]
