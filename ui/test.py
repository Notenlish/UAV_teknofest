import os
import sys

import pygame
import requests
from dotenv import load_dotenv

load_dotenv()

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Map Viewer")

# style z=zoom x y[optionally the scale modifier as well] scale file_format apikey
URL = "https://tile.thunderforest.com/{}/{}/{}/{}.{}?apikey={}"

# Tiles are available on zoom levels 0 through 22.


# Function to download a tile from OpenStreetMap
def download_tile(
    zoom, x, y, style="landscape", scale=1, file_format="png", cache_dir="ui/tiles"
):
    apikey = os.environ["THUNDERFOREST_API_KEY"]
    assert scale <= 2 and scale >= 1
    _y_str = f"{y}@{scale}x" if scale != 1 else y
    url = URL.format(style, zoom, x, _y_str, file_format, apikey)
    print(url)
    tile_path = os.path.join(
        cache_dir, f"{style}_{zoom}_{x}_{y}_{scale}x.{file_format}"
    )
    print(tile_path)  # idk why this works

    if not os.path.exists(tile_path):
        os.makedirs(cache_dir, exist_ok=True)
        response = requests.get(url)
        if response.ok:
            with open(tile_path, "wb") as file:
                file.write(response.content)
        else:
            print("ERROR!", str(response.content))

    return tile_path


# Function to get a tile (download if not cached)
def get_tile(
    zoom, x, y, style="landscape", scale=2, file_format="png", cache_dir="ui/tiles"
):
    tile_path = os.path.join(
        cache_dir, f"{style}_{zoom}_{x}_{y}_{scale}x.{file_format}"
    )

    if not os.path.exists(tile_path):
        tile_path = download_tile(zoom, x, y, scale=scale)

    return tile_path


# Function to load a tile into a Pygame surface
def load_tile(zoom, x, y, cache_dir="ui/tiles"):
    tile_path = get_tile(zoom, x, y, cache_dir)
    return pygame.image.load(tile_path)


if __name__ == "__main__":
    img = load_tile(zoom=0, x=0, y=0)
    print(img.get_size())
    screen.blit(img, (0, 0))
    clock = pygame.time.Clock()
    while True:
        screen.fill("black")

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                raise SystemExit

        clock.tick(60)
        screen.blit(img, (0, 0))
        pygame.display.update()