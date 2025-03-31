# -*- coding: utf-8 -*-
"""
This module provides a function to save a corpus to a file in JSON format.

Functions:
- save_corpus: Saves a given corpus dictionary to a specified file path.
"""

import json
from pathlib import Path


def save_corpus(corpus: dict, file_path: Path) -> None:
    """
    Saves the given corpus to a file in JSON format.

    Args:
        corpus (dict): The corpus to save.
        file_path (Path): The path to the file where the corpus will be saved.

    Returns:
        None
    """
    with open(file_path, "w") as file:
        json.dump(corpus, file)
