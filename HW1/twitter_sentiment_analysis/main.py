# -*- coding: utf-8 -*-
"""
This file provides a command-line interface for performing Twitter sentiment
analysis operations.

The operations include:
- Preprocessing raw data.
- Building a corpus from training data.
- Predicting sentiment using a given corpus.
- Evaluating the model with test data.

Each operation requires specific arguments, which are validated before execution.
"""

import argparse
import pandas as pd
from data.preprocessor import preprocess_data
from data.fetcher import fetch_data
from data.spliter import split_data
from data.loader import load_data
from data import RAW_DATA_PATH, FILE_NAME
import csv
from corpus.builder import build_corpus
from corpus.dumper import save_corpus
from corpus.loader import load_corpus
from corpus.predictor import predict_text
from corpus.evaluator import evaluate_corpus


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments for the script.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Twitter Sentiment Analysis")
    parser.add_argument(
        "--type",
        type=str,
        choices=["preprocess", "build", "predict", "evaluate"],
        required=True,
        help="Type of operation to perform. Options: 'preprocess', 'build', 'predict', 'evaluate'.",
    )

    # Build operation arguments
    parser.add_argument(
        "--build_data",
        type=str,
        help="[build] Path to the training data file for building the corpus.",
    )
    parser.add_argument(
        "--build_lemmatize",
        action="store_true",
        help="[build] Enable lemmatization during corpus building.",
    )
    parser.add_argument(
        "--build_remove",
        type=str,
        default="",
        help=(
            "[build] Comma-separated list of items to remove during corpus building. "
            "Options: 'stopwords', 'digits', 'special_characters', 'tags', 'urls', 'handles'."
        ),
    )
    parser.add_argument(
        "--build_out",
        type=str,
        help="[build] Path to the output file where the built corpus will be saved.",
    )

    # Predict operation arguments
    pred_group = parser.add_mutually_exclusive_group()
    pred_group.add_argument(
        "--pred_text",
        type=str,
        help="[predict] Text input for sentiment prediction.",
    )
    pred_group.add_argument(
        "--pred_data",
        type=str,
        help="[predict] Path to the data file for sentiment prediction.",
    )
    parser.add_argument(
        "--pred_corpus",
        type=str,
        help="[predict] Path to the corpus file to use for sentiment prediction.",
    )

    # Evaluate operation arguments
    parser.add_argument(
        "--eval_corpus",
        type=str,
        help="[evaluate] Path to the corpus file to use for model evaluation.",
    )
    parser.add_argument(
        "--eval_data",
        type=str,
        help="[evaluate] Path to the test data file to use for model evaluation.",
    )

    return parser.parse_args()


def handle_preprocess(args: argparse.Namespace) -> None:
    """
    Handles the 'preprocess' operation.

    Args:
        args (argparse.Namespace): Parsed arguments.
    """
    print(f"Downloading data...")
    fetch_data()
    print(f"Preprocessing data...")
    with open(RAW_DATA_PATH / FILE_NAME, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = pd.DataFrame(reader)
    data = preprocess_data(data)
    print(f"Splitting data...")
    split_data(data, 0.8)
    print(f"Data preprocessing completed.")


def handle_build(args: argparse.Namespace) -> None:
    """
    Handles the 'build' operation.

    Args:
        args (argparse.Namespace): Parsed arguments.
    """
    if not args.build_data:
        print("Error: --build_data is required for corpus building.")
        return
    if not args.build_out:
        print("Error: --build_out is required for saving the built corpus.")
        return
    print(f"Building the corpus with data: {args.build_data}")
    print(f"Lemmatize: {args.build_lemmatize}, Remove: {args.build_remove}")
    print(f"Output file: {args.build_out}")
    data = load_data(args.build_data)
    corpus = build_corpus(data, args.build_lemmatize, args.build_remove)
    save_corpus(corpus, args.build_out)
    print(f"Corpus built successfully and saved to: {args.build_out}")


def handle_predict(args: argparse.Namespace) -> None:
    """
    Handles the 'predict' operation.

    Args:
        args (argparse.Namespace): Parsed arguments.
    """
    if not args.pred_text and not args.pred_data:
        print("Error: Either --pred_text or --pred_data must be provided.")
        return
    if not args.pred_corpus:
        print("Error: --pred_corpus is required for prediction.")
        return
    input_source = args.pred_text or args.pred_data
    print(f"Predicting sentiment using input: {input_source}")
    print(f"Corpus file: {args.pred_corpus}")
    corpus = load_corpus(args.pred_corpus)
    if args.pred_text:
        prediction = predict_text(args.pred_text, corpus)
        print(f"text: {args.pred_text}, prediction: {prediction}")
    if args.pred_data:
        for text in load_data(args.pred_data)["Text"]:
            prediction = predict_text(text, corpus)
            print(f"text: {text}, prediction: {prediction}")


def handle_evaluate(args: argparse.Namespace) -> None:
    """
    Handles the 'evaluate' operation.

    Args:
        args (argparse.Namespace): Parsed arguments.
    """
    if not args.eval_corpus:
        print("Error: --eval_corpus is required for model evaluation.")
        return
    if not args.eval_data:
        print("Error: --eval_data is required for model evaluation.")
        return
    print(f"Evaluating the model with corpus: {args.eval_corpus}")
    print(f"Test data file: {args.eval_data}")
    corpus = load_corpus(args.eval_corpus)
    data = load_data(args.eval_data)
    evaluate_corpus(corpus, data)


if __name__ == "__main__":
    args = parse_arguments()
    if args.type == "preprocess":
        handle_preprocess(args)
    if args.type == "build":
        handle_build(args)
    if args.type == "predict":
        handle_predict(args)
    if args.type == "evaluate":
        handle_evaluate(args)
