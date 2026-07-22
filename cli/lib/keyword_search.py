import json 
import string
import os 
import pickle

from lib.search_utils import load_movies, load_stopwords, CACHE_PATH
from nltk.stem import PorterStemmer
from collections import defaultdict


stemmer = PorterStemmer()


class InvertedIndex: 
    def __init__(self):
        self.index = defaultdict(set) 
        self.docmap = defaultdict(set) 
        self.index_path = CACHE_PATH / 'index.pkl'
        self.docmap_path = CACHE_PATH / 'docmap.pkl'    
    
    def __add_document(self, doc_id, text): 
        tokens = tokenize_text(text)
        for token in set(tokens):
            self.index[token].add(doc_id)
    
    def get_documents(self, term): 
        return sorted(self.index.get(term, []))

    def build(self): 
        movies = load_movies()
        for movie in movies: 
            doc_id = movie['id']
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id, text)
            self.docmap[doc_id] = movie  
    
    def load(self): 
        if not self.index_path.exists() or not self.docmap_path.exists(): 
            raise FileNotFoundError('Index files not found')
        with open(self.index_path, 'rb') as f:
            self.index = pickle.load(f)
        with open(self.docmap_path, 'rb') as f: 
            self.docmap = pickle.load(f)


    def save(self): 
        os.makedirs(CACHE_PATH, exist_ok = True)

        with open(self.index_path, 'wb') as f: 
            pickle.dump(self.index, f)

        with open(self.docmap_path, 'wb') as f: 
            pickle.dump(self.docmap, f)





def clean_text(text:str) -> str:
    return text.lower().translate(str.maketrans('','',string.punctuation))

def tokenize_text(text:str) -> list[str]:
    text = clean_text(text)
    words = text.split()
    stopwords = load_stopwords()
    filtered = [stemmer.stem(word) for word in words if word not in stopwords]
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
    movie_index = InvertedIndex()

    try: 
        movie_index.load()
        results = []
        for token in query_tokens:
            doc_ids = movie_index.get_documents(token)
            for doc_id in doc_ids:
                if doc_id not in results: 
                    results.append(doc_id)
                if len(results) >= 5: 
                    break
            if len(results) >= 5:
                break

        for doc_id in results: 
            movie = movie_index.docmap[doc_id]
            print(f"{movie['id']}: {movie['title']}")
    except FileNotFoundError: 
        print("Index Not Found. Please run build first")
        return

 