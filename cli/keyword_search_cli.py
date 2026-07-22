#!/usr/bin/env python3
import argparse
from lib.keyword_search import keyword_search, InvertedIndex

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    build_inverted_index = subparsers.add_parser("build", help="load the movie data")     
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
             # print the search query 
           keyword_search(query=args.query)               
        case "build": 
            index = InvertedIndex()
            index.build()                    
            index.save()
            docs = index.get_documents('merida')
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()