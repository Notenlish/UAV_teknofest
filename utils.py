import json

def read_config(file: str = None):
    if file is None:
        raise ValueError("None value for string path")
    with open(file, "r") as f:
        data = json.load(f)
    return data

