import json 
from pathlib import Path 

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "movies.json" 
STOPWORDS_PATH = PROJECT_ROOT / "data" / "stopwords.txt" 
CACHE_PATH = PROJECT_ROOT / 'cache'


def load_movies() -> list[dict]: 
    try: 
        with open(DATA_PATH, "r") as file: 
            data = json.load(file)
            return data["movies"]
    except FileNotFoundError: 
        return { "movies": [] } 


def load_stopwords() -> list[str]: 
    try:
        with open(STOPWORDS_PATH, "r") as file: 
            return [line.strip() for line in file] 
    except FileNotFoundError: 
        return []