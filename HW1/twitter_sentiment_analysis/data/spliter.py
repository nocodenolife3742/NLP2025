"""
Splits the dataset into training and testing sets based on a specified ratio.'

Functions:
- split_data: Splits the dataset into training and testing sets and saves them to CSV files.'
"""

import pandas as pd
from . import PROCESSED_DATA_PATH, TRAIN_FILE_NAME, TEST_FILE_NAME


def split_data(data: pd.DataFrame, train_size: float = 0.8) -> None:
    """
    Splits the dataset into training and testing sets based on the specified ratio.

    Args:
        data (pd.DataFrame): The input dataset to split.
        train_size (float): The ratio of training data to total data (default: 0.8).
    """
    train_data = data.sample(frac=train_size)
    test_data = data.drop(train_data.index)

    train_data.to_csv(PROCESSED_DATA_PATH / TRAIN_FILE_NAME, index=False)
    test_data.to_csv(PROCESSED_DATA_PATH / TEST_FILE_NAME, index=False)
