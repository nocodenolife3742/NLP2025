# -*- coding: utf-8 -*-
"""
This script loads a corpus from a file.

The corpus is expected to be in JSON format.
"""

import json
from pathlib import Path


def load_corpus(file_path: Path) -> dict:
    """
    Load a corpus from a JSON file.

    Args:
        file_path (Path): The path to the corpus file.

    Returns:
        dict: The loaded corpus.
    """
    with open(file_path, "r") as file:
        return json.load(file)
