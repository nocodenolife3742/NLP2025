# -*- coding: utf-8 -*-
"""
This module fetches data from a specified URL and saves it to a local file.
It is designed to be used as part of a larger data processing pipeline for sentiment analysis.

Functions:
- fetch_data: Fetches data from a given URL and saves it to a local file.
"""

import requests
from pathlib import Path
from zipfile import ZipFile
from tqdm import tqdm
from . import RAW_DATA_PATH

DATA_URL = (
    "http://thinknook.com/wp-content/uploads/2012/09/Sentiment-Analysis-Dataset.zip"
)


def fetch_data() -> None:
    """
    Fetch data from a given URL and save it to a local file.

    This function downloads a zip file from the specified URL, extracts its contents,
    and saves the extracted files to a local directory.

    Args:
        None

    Returns:
        None
    """
    try:
        with requests.get(DATA_URL, stream=True) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
            with open("temp.zip", "wb") as temp_file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    temp_file.write(data)
            progress_bar.close()
            if total_size != 0 and progress_bar.n != total_size:
                print("ERROR, something went wrong")
        with ZipFile("temp.zip") as zip_file:
            zip_file.extractall(RAW_DATA_PATH)
        Path("temp.zip").unlink()
        print(f"Data fetched and saved to {RAW_DATA_PATH}.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
