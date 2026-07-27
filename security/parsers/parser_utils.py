import json
from pathlib import Path
from dataclasses import asdict


def load_json(file_path: str):
    """
    Load a JSON report from disk.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, output_path: str):
    """
    Save normalized JSON to disk.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def dataclass_to_dict(obj):
    """
    Convert dataclass object into dictionary.
    """
    return asdict(obj)
