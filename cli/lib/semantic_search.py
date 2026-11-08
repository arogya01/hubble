from sentence_transformers import SentenceTransformer 
import numpy as np
import os
from lib.search_utils import CACHE_PATH, load_movies, load_stopwords


class SemanticSearch: 
    def __init__(self): 
        self.model = SentenceTransformer("all-MiniLM-L6-v2") 
        self.embeddings = None 
        self.documents = None 
        self.document_map = {}

    def generate_embedding(self, text): 
        if not text or not text.strip(): 
            raise ValueError("Text cannot be empty or only whitespace")
        embeddings = self.model.encode([text])
        return embeddings[0]

    def build_embeddings(self, documents): 
        self.documents = documents 
        movie_strings = []
        for doc in documents: 
            self.document_map[doc["id"]] = doc 
            movie_strings.append(f"{doc['title']}: {doc['description']}")
        self.embeddings = self.model.encode(movie_strings, show_progress_bar = True)
        np.save("cache/movie_embeddings.npy", self.embeddings)
        return self.embeddings
    
    def load_or_create_embeddings(self, documents): 
        self.documents = documents 
        for doc in documents: 
            self.document_map[doc["id"]] = doc 
        if os.path.exists("cache/movie_embeddings.npy"): 
            self.embeddings = np.load("cache/movie_embeddings.npy")
            if len(self.embeddings) == len(documents): 
                return self.embeddings
        
        return self.build_embeddings(documents)


def embed_query_text(query: str): 
        search = SemanticSearch()
        embedding = search.generate_embedding(query)
        print(f"Query: {query}")
        print(f"First 3 dimensions: {embedding[:3]}")
        print(f"Shape: {embedding.shape}")

def cosine_similarity(vec1,vec2): 
    dot_product = np.dot(vec1,vec2) 
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def verify_embeddings(): 
    search = SemanticSearch()
    documents = load_movies()
    embeddings = search.load_or_create_embeddings(documents)
    print(f"Number of docs: {len(documents)}")
    print(f"Embeddings shape: {embeddings.shape[0]} vectors in {embeddings.shape[1]} dimensions")
        

def embed_text(text): 
    search = SemanticSearch()
    embedding = search.generate_embedding(text)
    print(f"Text: {text}")
    print(f"First 3 Dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")


def verify_model(): 
    search = SemanticSearch()
    print(f"Model loaded: {search.model}")
    print(f"Max sequence length: {search.model.max_seq_length}")


def add_vectors(vec1: list[float], vec2: list[float]) -> list[float]: 
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have the same length")
    
    result = []

    for i in range(len(vec1)): 
        result.append(vec1[i] + vec2[i])

    return result

def subtract_vectors(vec1 : list[float], vec2: list[float]) -> list[float]:
    if len(vec1) != len(vec2): 
        raise ValueError("Vectors must be the same length")

    result = []

    for i in range(len(vec1)): 
        result.append(vec1[i] - vec2[i])
    
    return result

def dot_product(vec1: list[float], vec:list[float])-> list[float]: 
    if len(vec1) != len(vec2): 
        raise ValueError("Vectors must be the same length")

    result = []

    for i in range(len(vec1)): 
        result+=(vec1[i] * vec2[i]) 
        

if __name__ == "__main__":
    # Test movie vectors
    great_bear = [0.5, -0.2, 0.8]
    back_country = [0.1, 0.9, -0.3]
    revenant = [0.1, 0.9, -0.3]

    print("--- 1. Testing Vector Addition ---")
    combined = add_vectors(great_bear, back_country)
    print(f"{great_bear} + {back_country}")
    print(f"=> Result: {[round(x, 2) for x in combined]}\n")

    print("--- 2. Testing Vector Subtraction ---")
    filtered = subtract_vectors(great_bear, revenant)
    print(f"{great_bear} - {revenant}")
    print(f"=> Result: {[round(x, 2) for x in filtered]}\n")

    print("--- 3. Testing Error Handling ---")
    try:
        add_vectors([1.0, 2.0], [1.0])
    except ValueError as e:
        print(f"Caught expected error: {e}")


