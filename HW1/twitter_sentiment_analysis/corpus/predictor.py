# -*- coding: utf-8 -*-
"""
This module provides a function to predict the sentiment of a given text using a given corpus.

Functions:
- predict_text: Predicts the sentiment of the given text using the given corpus.
"""

import nltk
from math import log


def predict_text(text: str, corpus: dict) -> str:
    """
    Predicts the sentiment of the given text using the given corpus.

    Args:
        text (str): The text to predict the sentiment of.
        corpus (dict): The corpus to use for sentiment prediction.

    Returns:
        str: The predicted sentiment.
    """

    tokens = nltk.TweetTokenizer().tokenize(text)
    positive = log(corpus["stats"]["positive_tweets"]) - log(corpus["stats"]["total_tweets"])
    negative = log(corpus["stats"]["negative_tweets"]) - log(corpus["stats"]["total_tweets"])
    for token in tokens:
        if token in corpus["words"]:
            positive += log(corpus["words"][token]["positive"]) - log(corpus["stats"]["positive_words"])
            negative += log(corpus["words"][token]["negative"]) - log(corpus["stats"]["negative_words"])
    return "positive" if positive > negative else "negative"
