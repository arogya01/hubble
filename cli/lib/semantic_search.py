from sentence_transformers import SentenceTransformer 



class SemanticSearch: 
    def __init__(self): 
        self.model = SentenceTransformer("all-MiniLM-L6-v2")


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


