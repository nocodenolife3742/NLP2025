# -*- coding: utf-8 -*-
"""
This script loads and preprocesses the Twitter Sentiment Analysis dataset.

The preprocessing steps include:
- Loading the dataset from the processed directory.
- Decoding HTML entities in the text column.
"""

import pandas as pd
from pathlib import Path
import html


def load_data(file_path: Path) -> pd.DataFrame:
    """
    Loads and preprocesses the dataset by decoding HTML entities.

    Args:
        file_path (Path): The path to the dataset file.

    Returns:
        pd.DataFrame: The loaded and preprocessed dataset.
    """
    data = pd.read_csv(file_path)
    data["Text"] = data["Text"].apply(html.unescape)
    return data
