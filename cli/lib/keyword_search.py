
import json 
import string
from lib.search_utils import load_movies, load_stopwords

def clean_text(text:str) -> str:
    return text.lower().translate(str.maketrans('','',string.punctuation))

def tokenize_text(text:str) -> list[str]:
    text = clean_text(text)
    words = text.split()
    stopwords = load_stopwords()
    filtered = [word for word in words if word not in stopwords]
    return filtered 

def has_matching_token(query_toks:list[str],movie_toks:list[str]) -> bool:
    for query_tok in query_toks:
        for movie_tok in movie_toks: 
            if query_tok in movie_tok:
                return True
    return False


def keyword_search(query:str) -> None:
    print(f"Searching for: {query}")
    query_tokens = tokenize_text(query)
    print(f"Search Query: {query_tokens}")
    movie_data = load_movies()
    for index, movie in enumerate(movie_data["movies"]):
        movie_tokens = tokenize_text(movie["title"])
        if has_matching_token(query_toks = query_tokens,movie_toks = movie_tokens):
            print(f"{index + 1}. {movie}") 
 