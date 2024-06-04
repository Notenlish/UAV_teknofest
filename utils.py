from pygame import Rect
import json


def read_config(file: str = None):
    if file is None:
        raise ValueError("None value for string path")
    with open(file, "r") as f:
        data = json.load(f)
    return data


def hash_pg_rect(rect: Rect):
    return hash((rect.x, rect.y, rect.w, rect.h))
