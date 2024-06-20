import json

from pyproj import Proj, transform

# https://epsg.io/3857
web_mercator = Proj(init="epsg:3857")


import pygame

pygame.font.init()


def read_config(file: str = None):
    if file is None:
        raise ValueError("None value for string path")
    with open(file, "r") as f:
        data = json.load(f)
    return data


# taken from https://stackoverflow.com/questions/15098900/how-to-set-the-pivot-point-center-of-rotation-for-pygame-transform-rotate
def rotate(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)
    rotated_offset = offset.rotate(angle)
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect


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
    # calculate sep width and height
    row1 = texts[0]
    combined = "".join(texts[0])
    combined_rect = get_text_rect(font, combined)
    diff_w = table_rect.w - combined_rect.w
    diff_h = table_rect.h - combined_rect.h
    sep_w = diff_w / len(row1)
    sep_h = diff_h / len(row1)

    point = pygame.Rect(table_rect.topleft, (1, 1))
    row_rects: list[pygame.Rect] = []

    point.move(sep_w, 0)
    for text in row1:
        rect = get_text_rect(font, text)
        rect = rect.move(point.x, 0)
        row_rects.append(rect)
        point.x += rect.w
        point.y += rect.h
        point.x += sep_w
        point.y += sep_w

    y = row_rects[0].y
    for row in texts:
        for i, text in enumerate(row):
            rect = get_text_rect(font, text)
            rect.center = row_rects[i].center
            rect.y = y
            draw_text(
                screen, font, text, rect.center, text_color, anchor=("center", "center")
            )
        y += row_rects[0].h + sep_h


def lat_lon_to_web_mercator(lat, lon):
    """NOTE: The web mercator projection is limited by the poles because earth isnt perfectly round. So you cant use this for the north pole or smth

    Args:
        lat (_type_): _description_
        lon (_type_): _description_

    Returns:
        x: as in meters away from center of equator(i think) between -20037508.34 to 20037508.34 meters
        y: as in meters away from center of equator(i think) between -20037508.34 to 20037508.34 meters
    """
    # Transform the latitude and longitude to Web Mercator x, y coordinates
    x, y = web_mercator(lon, lat)
    return x, y
