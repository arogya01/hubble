import argparse
from lib.semantic_search import embed_query_text, embed_text, verify_model, verify_embeddings


def main() -> None:
    parser = argparse.ArgumentParser(description="Semantic Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    subparsers.add_parser("verify", help="Verify model loading")
    subparsers.add_parser("verify_embeddings", help="Verify document embeddings")
    embed_query_parser = subparsers.add_parser("embed_query", help="Embed Query Text")

    embed_parser = subparsers.add_parser("embed_text", help="Embed Text")
    embed_parser.add_argument("text", type=str, help="Text to embed")
    embed_query_parser.add_argument("query", type=str, help="Text to query")


    args = parser.parse_args()

    match args.command:
        case "verify":
            verify_model()
        case "embed_text":
            embed_text(args.text)
        case "verify_embeddings":
            verify_embeddings()
        case "embed_query": 
            embed_query_text(args.query)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
