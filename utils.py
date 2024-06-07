import json

import pygame

pygame.font.init()


def read_config(file: str = None):
    if file is None:
        raise ValueError("None value for string path")
    with open(file, "r") as f:
        data = json.load(f)
    return data


def position_anchor(rect: pygame.Rect | pygame.FRect, anchor: tuple[str, str]):
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


def hash_pg_rect(rect: pygame.Rect):
    return hash((rect.x, rect.y, rect.w, rect.h))


def get_text_rect(font: pygame.Font, text, antialias=True, color="black"):
    surf = font.render(text, antialias=antialias, color=color)
    return surf.get_rect()


def draw_text(
    screen,
    font: pygame.Font,
    text,
    point: tuple[float, float],
    color="black",
    anchor: tuple[str, str] = ("center", "center"),
):
    if type(text) != bytes and type(text) != str:
        text = str(text)
    rect = get_text_rect(font, text, antialias=True, color=color)
    surf = font.render(text, antialias=True, color=color)
    anchor = position_anchor(rect, anchor)
    anchor = (anchor[0] + point[0], anchor[1] + point[1])
    screen.blit(surf, anchor)
    return rect


def draw_table(
    screen,
    font,
    texts: list[list[str]],
    table_rect: pygame.Rect,
    text_color="black",
    sep_color="white",
):
    row1 = texts[0]
    point = pygame.Rect(table_rect.topleft, (1, 1))
    row_rects = []
    for text in row1:
        rect = get_text_rect(font, text)
        # rect = rect.move(table_rect.topleft)
        rect = rect.move(point.x, 0)
        row_rects.append(rect)
        point.x += rect.w
        point.y += rect.h

    sum_rect = pygame.Rect(*table_rect.topleft, 0, 0)
    for rect in row_rects:
        sum_rect.w += rect.w
        sum_rect.h += rect.h

    sep_count = len(texts[0]) + 1
    sep_width = (table_rect.w - sum_rect.w) / sep_count

    point = pygame.Rect(*table_rect.topleft, 0, 0)
    for j, row in enumerate(texts):
        point.x = table_rect.left + sep_width
        for i, text in enumerate(row):
            text_rect = get_text_rect(font, text, antialias=True, color=text_color)
            row_text = texts[0][i]
            container = row_rects[i]

            if j == 1 and 0 == 1:
                container.x = point.x
                pygame.draw.rect(screen, (i * 42, i * 42, i * 42), container, width=3)

            # text_rect.center = container.center
            draw_text(
                screen,
                font,
                text,
                point.move(0, container.h / 2).topleft,
                text_color,
                anchor=("center", "center") if j != 0 else ("left", "top"),
            )

            point[0] += sep_width + container.w
        point[1] += sep_width + container.h
