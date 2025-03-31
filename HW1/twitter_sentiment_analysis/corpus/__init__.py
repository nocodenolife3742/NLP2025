import nltk
import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
NLTK_DATA_DIR = CURRENT_DIR / "nltk_data"

nltk.data.path.append(NLTK_DATA_DIR)
nltk.download("wordnet", quiet=True, download_dir=NLTK_DATA_DIR)
nltk.download("stopwords", quiet=True, download_dir=NLTK_DATA_DIR)

stopwords = set(nltk.corpus.stopwords.words("english"))
