# -*- coding: utf-8 -*-
"""
This module provides functions to preprocess text data and build a sentiment-based corpus.

Functions:
- tokenize: Tokenizes and preprocesses input text based on specified options.
- build_corpus: Constructs a sentiment-based token corpus from input data.
"""

import pandas as pd
import nltk
from tqdm import tqdm
from . import stopwords


def is_all_special_characters(token: str) -> bool:
    """
    Checks if the input token consists of all special characters.

    Args:
        token (str): The input token.

    Returns:
        bool: True if the token consists of all special characters, False otherwise.
    """
    return bool(token) and all(not char.isalnum() for char in token)


def tokenize(string: str, lemmatize: bool, remove: str) -> list:
    """
    Tokenizes the input string.

    Args:
        string (str): The input string.
        lemmatize (bool): Whether to lemmatize the text.
        remove (str): The items to remove from the text. Options include:
            - "stopwords": Remove stopwords.
            - "digits": Remove numeric tokens.
            - "special_characters": Remove non-alphanumeric tokens.
            - "tags": Remove hashtags.
            - "urls": Remove URLs.
            - "handles": Remove user handles.

    Returns:
        list: The tokenized string.
    """
    # Tokenize the input string using TweetTokenizer
    tokens = nltk.tokenize.TweetTokenizer().tokenize(string)

    # Apply lemmatization if specified
    if lemmatize:
        lemmatizer = nltk.stem.WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Remove specified items from the tokens
    if remove:
        remove_options = remove.split(",")
        if "stopwords" in remove_options:
            tokens = [token for token in tokens if token not in stopwords]
        if "digits" in remove_options:
            tokens = [token for token in tokens if not token.isdigit()]
        if "special_characters" in remove_options:
            tokens = [token for token in tokens if not is_all_special_characters(token)]
        if "tags" in remove_options:
            tokens = [token for token in tokens if not token.startswith("#")]
        if "urls" in remove_options:
            tokens = [token for token in tokens if not token.startswith("http")]
        if "handles" in remove_options:
            tokens = [token for token in tokens if not token.startswith("@")]

    return tokens


def build_corpus(data: pd.DataFrame, lemmatize: bool, remove: str) -> dict:
    """
    Builds a corpus from the input data.

    Args:
        data (pd.DataFrame): The input data.
        lemmatize (bool): Whether to lemmatize the text.
        remove (str): The items to remove from the text.

    Returns:
        dict: The built corpus.
    """
    words = {}
    positive_words = 0
    negative_words = 0
    positive_tweets = data[data["Sentiment"] == 1].shape[0] + 1  # Laplace smoothing
    negative_tweets = data[data["Sentiment"] == 0].shape[0] + 1  # Laplace smoothing
    for sentiment, text in tqdm(
        data[["Sentiment", "Text"]].values, desc="Building Corpus"
    ):
        tokens = tokenize(text, lemmatize, remove)
        for token in tokens:
            if token not in words:
                words[token] = {"positive": 1, "negative": 1}  # Laplace smoothing
                positive_words += 1
                negative_words += 1
            if sentiment == 1:
                words[token]["positive"] += 1
                positive_words += 1
            else:
                words[token]["negative"] += 1
                negative_words += 1
    corpus = {
        "stats": {
            "positive_words": positive_words,
            "negative_words": negative_words,
            "total_words": positive_words + negative_words,
            "positive_tweets": positive_tweets,
            "negative_tweets": negative_tweets,
            "total_tweets": positive_tweets + negative_tweets,
        }
    }
    corpus["words"] = words
    return corpus
