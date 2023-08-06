from pathlib import Path
from typing import NoReturn

import yaml
from yaml.parser import ParserError
from yaml.scanner import ScannerError


def trim_text(raw: str, max_length: int) -> str:
    """Given a max length for a text, limit text to the same if it exceeds the length"""
    return raw[:max_length] if len(raw) > max_length else raw


def load_yaml_from_path(file_path: Path):
    """Load the contents of the .yaml file"""
    with open(file_path, "r") as readfile:
        return yaml.load(readfile, Loader=yaml.FullLoader)


def load_yaml_list(file_path: Path) -> NoReturn | list:
    """Load contents of the .yaml file only if it is a valid list"""
    try:
        d = load_yaml_from_path(file_path)
        if isinstance(d, list):
            return d
        raise Exception("Should be a list")
    except ScannerError as e:
        raise Exception(f"See error {e}")
    except ParserError as e:
        raise Exception(f"See error {e}")
