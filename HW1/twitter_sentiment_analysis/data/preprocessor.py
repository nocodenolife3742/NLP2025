# -*- coding: utf-8 -*-
"""
This script preprocesses the Twitter Sentiment Analysis dataset.

Functions:
- preprocess_data: Cleans and preprocesses the dataset for sentiment analysis.
"""

import pandas as pd


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and preprocesses the dataset for sentiment analysis.

    This function removes unnecessary columns, renames columns for consistency,
    and processes the text data to ensure uniform formatting.

    Args:
        data (pd.DataFrame): The raw input dataset.

    Returns:
        pd.DataFrame: The cleaned and preprocessed dataset ready for analysis.
    """
    columns_to_keep = ["Sentiment", "SentimentText"]
    data = data[columns_to_keep]
    data.columns = ["Sentiment", "Text"]
    data.loc[:, "Text"] = data["Text"].str.lower().str.strip()
    return data
