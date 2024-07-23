
import pygame


class CommandPanel:
    def __init__(self, ui, config: dict[str, any], screen_area: pygame.Rect) -> None:
        self.ui = ui
        self.screen_area = screen_area

        self.icon_size = (40, 40)

        self.bg_col = config["window"]["windowBackground"]

        self.commands = config["window"]["windowCommands"]
        self._load_images()

    def test_events(self, m_just_pressed):
        if m_just_pressed[0]:
            for item in self.commands:
                item:dict
                rect: pygame.Rect = item["rect"]
                if rect.collidepoint(*pygame.mouse.get_pos()):
                    func = item.get("function", lambda: None)
                    exec(f"self.ui.app.{func}()")

    def _load_images(self):
        pos = [self.screen_area.centerx - (self.icon_size[0] // 2), 10]
        for i, item in enumerate(self.commands):
            path: str = item["imagePath"]
            rect = pygame.Rect(*pos, *self.icon_size)

            if i % 2:
                pos[0] += self.icon_size[0] + 10
            else:
                pos[0] -= self.icon_size[0] + 10

            if path.endswith("png") or path.endswith("jpg") or path.endswith("jpeg"):
                image = pygame.image.load(path)
            elif path.endswith("svg"):
                image = pygame.image.load_sized_svg(path, self.icon_size)
            else:
                image = pygame.transform.scale(
                    pygame.image.load("ui/data/empty.png"), self.icon_size
                )
            self.commands[i]["image"] = image
            self.commands[i]["rect"] = rect

            if i % 2 == 1:
                pos[1] += 15 + item["image"].get_size()[1]

    def render(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.bg_col, self.screen_area)

        for item in self.commands:
            rect:pygame.Rect = item["rect"]
            # rect.move_ip(5, 5)
            pygame.draw.rect(screen, "white", rect.inflate(5, 5))
            screen.blit(item["image"], rect.topleft)
