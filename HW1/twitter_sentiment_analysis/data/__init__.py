from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1].parent.resolve()
DATA_DIR = PROJECT_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "raw"
PROCESSED_DATA_PATH = DATA_DIR / "processed"
FILE_NAME = "Sentiment Analysis Dataset.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

