import json 
from pathlib import Path 

PROJECT_ROOT = Path(__file__).resolve().parents(2)
DATA_PATH = PROJECT_ROOT / "data" / "movies.json" 

def load_movies() -> List[dict]: 
    try: 
        with open(DATA_PATH, "r") as file: 
            data = json.load(file)
            return data["movies"]
    except FileNotFoundError: 
        return { "movies": [] } 

