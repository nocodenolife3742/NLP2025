# -*- coding: utf-8 -*-
"""
This module provides functions to evaluate the sentiment prediction accuracy of a corpus.

Functions:
- evaluate_corpus: Evaluates the sentiment prediction accuracy of a given corpus using the given data.
"""

import pandas as pd
from corpus.predictor import predict_text
from tqdm import tqdm


def evaluate_corpus(corpus: dict, data: pd.DataFrame) -> None:
    """
    Evaluates the sentiment prediction accuracy, precision, recall, and
    F1 score of the given corpus using the given data.

    Args:
        corpus (dict): The corpus to evaluate.
        data (pd.DataFrame): The data to use for evaluation.

    Returns:
        None
    """

    true_positives = 0
    false_positives = 0
    true_negatives = 0
    false_negatives = 0

    for sentiment, text in tqdm(data[["Sentiment", "Text"]].values, desc="Evaluating"):
        prediction = predict_text(text, corpus)
        if sentiment == 1 and prediction == "positive":
            true_positives += 1
        if sentiment == 1 and prediction == "negative":
            false_negatives += 1
        if sentiment == 0 and prediction == "positive":
            false_positives += 1
        if sentiment == 0 and prediction == "negative":
            true_negatives += 1

    accuracy = (true_positives + true_negatives) / len(data)
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1_score = 2 * (precision * recall) / (precision + recall)

    print("Evaluation Results:")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1_score:.2f}")
