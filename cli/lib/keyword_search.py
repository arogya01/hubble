
import json 
from lib.search_utils import load_movies


with open("data/movies.json", "r") as file: 
    movie_data = json.load(file)


def keyword_search(query:str) -> None:
    print(f"Searching for: {query}")
    search_query = query.lower().split()
    print(f"Search Query: {search_query}")
    for index, movie in enumerate(movie_data["movies"]):
        movie_title_lower = movie["title"].lower()
        if any(word in movie_title_lower for word in search_query) :
            print(f"{index + 1}. {movie}")  
 