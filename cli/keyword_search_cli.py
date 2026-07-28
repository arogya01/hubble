#!/usr/bin/env python3
import argparse
from lib.keyword_search import keyword_search, InvertedIndex, tokenize_single_term

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    build_inverted_index = subparsers.add_parser("build", help="load the movie data")     
    tf_inverted_index = subparsers.add_parser("tf",help="get the term freq")
    idf_parser = subparsers.add_parser("idf",help="Calculate IDF for a term")
    tfidf_parser=subparsers.add_parser("tfidf",help="Calculate the TFIDF for a term")
    
    search_parser.add_argument("query", type=str, help="Search query")
    tf_inverted_index.add_argument("doc_id", type=int, help = "Document ID")
    tf_inverted_index.add_argument("term", type=str, help="Search term")
    idf_parser.add_argument("term", type=str, help="calculate the TF-IDF for the term")
    tfidf_parser.add_argument("doc_id", type=int, help="Document ID")
    tfidf_parser.add_argument("term", type=str, help="Search term")



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
        case "tf": 
            index = InvertedIndex()
            index.load()
            clean_token = tokenize_single_term(args.term)
            tf_count = index.get_tf(args.doc_id,clean_token)
            print(tf_count)
        case "idf": 
            index = InvertedIndex()
            index.load()
            clean_token = tokenize_single_term(args.term)
            idf = index.get_idf(clean_token)
            print(f"Inverse document frequency of '{args.term}': {idf:.2f}")
        case "tfidf":
            index = InvertedIndex()
            index.load()
            clean_token = tokenize_single_term(args.term)
            tf = index.get_tf(args.doc_id,clean_token)
            idf = index.get_idf(clean_token)
            tf_idf = tf * idf
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tf_idf:.2f}")
        case _:
            parser.print_help()

if __name__ == "__main__":
    main()