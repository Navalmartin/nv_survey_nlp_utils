import json
from pathlib import Path


def read_json(filename: Path) -> dict:

    with open(filename, 'r') as f:
        return json.load(f)