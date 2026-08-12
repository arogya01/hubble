import json 
import string
import os 
import pickle
import math

from lib.search_utils import load_movies, load_stopwords, CACHE_PATH
from nltk.stem import PorterStemmer
from collections import defaultdict, Counter
stemmer = PorterStemmer()


BM25_K1 = 1.5
BM25_B = 0.75


class InvertedIndex: 
    def __init__(self):
        self.index = defaultdict(set) 
        self.docmap = defaultdict(set) 
        self.term_freq = defaultdict(Counter)
        self.doc_lengths = defaultdict(Counter)
        self.index_path = CACHE_PATH / 'index.pkl'
        self.docmap_path = CACHE_PATH / 'docmap.pkl'    
        self.term_freq_path = CACHE_PATH / 'term_freq.pkl'
        self.doc_lengths_path = CACHE_PATH / "doc_lengths.pkl"
    
    def __add_document(self, doc_id, text): 
        tokens = tokenize_text(text)
        for token in tokens: 
            self.term_freq[doc_id][token] += 1
            self.index[token].add(doc_id)
        self.doc_lengths[doc_id] = len(tokens)
    
    def get_documents(self, term): 
        return sorted(self.index.get(term, []))

    def build(self): 
        movies = load_movies()
        for movie in movies: 
            doc_id = movie['id']
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id, text)
            self.docmap[doc_id] = movie  
    
    def get_tf(self,doc_id,term):
        return self.term_freq.get(doc_id,{}).get(term,0)
    
    def get_idf(self, term: str) -> float:
        total_doc_count = len(self.docmap)
        term_match_doc_count = len(self.get_documents(term))
        return math.log((total_doc_count + 1) / (term_match_doc_count + 1))

    def get_bm25_idf(self, term:str) -> float:
        total_doc_count = len(self.docmap)
        term_match_doc_count = len(self.get_documents(term))
        return math.log((total_doc_count - term_match_doc_count + 0.5) / (term_match_doc_count + 0.5) + 1)  

    def bm25_search(self, query, limit = 5): 
        # for every query we're getting a bm25 score. 
        query_tokens = tokenize_text(query)
        scores = {}
        for doc_id in self.docmap: 
            total_score = 0.0 

            for token in query_tokens: 
                total_score += self.bm25(doc_id, token)
        
            scores[doc_id] = total_score
        
        sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        return sorted_docs[:limit]



    def bm25(self, doc_id, term):
        return round(self.get_bm25_tf(doc_id, term) * self.get_bm25_idf(term), 2)

    def __get_avg_doc_length(self) -> float: 
        if len(self.doc_lengths) == 0:
            return 0.0
        return sum(self.doc_lengths.values()) / len(self.doc_lengths)

    def get_bm25_tf(self, doc_id, term:str, k1 = BM25_K1, b = BM25_B) -> float: 
        tf = self.get_tf(doc_id, term)
        doc_length = self.doc_lengths[doc_id]
        avg_doc_length = self.__get_avg_doc_length()
        length_norm = 1 - b + b * (doc_length / avg_doc_length)
        return (tf * (k1 + 1)) / (tf + k1 * length_norm)

    def load(self): 
        if not self.index_path.exists() or not self.docmap_path.exists(): 
            raise FileNotFoundError('Index files not found')
        with open(self.index_path, 'rb') as f:
            self.index = pickle.load(f)
        with open(self.docmap_path, 'rb') as f: 
            self.docmap = pickle.load(f)
        with open(self.term_freq_path, 'rb') as f: 
            self.term_freq = pickle.load(f)
        with open(self.doc_lengths_path, 'rb') as f: 
            self.doc_lengths = pickle.load(f)


    def save(self): 
        os.makedirs(CACHE_PATH, exist_ok = True)

        with open(self.index_path, 'wb') as f: 
            pickle.dump(self.index, f)

        with open(self.docmap_path, 'wb') as f: 
            pickle.dump(self.docmap, f)

        with open(self.term_freq_path, 'wb') as f: 
            pickle.dump(self.term_freq, f)
        
        with open(self.doc_lengths_path, 'wb') as f: 
            pickle.dump(self.doc_lengths, f)




def tokenize_single_term(term): 
    tok = tokenize_text(term)
    if len(tok) != 1: 
        raise ValueError(f"Term '{term}' must result in exactly 1 token, got {len(tok)}")
    return tok[0]

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

 