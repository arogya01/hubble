# rag-search-engine

A from-scratch search engine over a movie corpus. Keyword search (inverted index →
TF-IDF → BM25) and semantic search (sentence embeddings + cosine similarity), built
up step by step with an interactive HTML explainer for each concept.

## Quickstart

```bash
uv sync                              # installs runtime + dev deps into .venv
uv run python cli/keyword_search_cli.py build          # build the inverted index
uv run python cli/keyword_search_cli.py bm25search "dinosaur"
uv run python cli/semantic_search_cli.py verify        # download/load the embedding model
```

`uv run` always uses the project venv, so nothing needs to be activated by hand.

## Everyday commands

| What | Command |
| --- | --- |
| Lint | `uv run ruff check cli` |
| Lint + autofix (imports, whitespace) | `uv run ruff check --fix cli` |
| Format | `uv run ruff format cli` |
| Type check | `uv run pyright` |
| Tests | `uv run pytest` |
| Run anything | `uv run python cli/...` |

## Layout

```
cli/
  keyword_search_cli.py   argparse entry point for keyword search
  semantic_search_cli.py  argparse entry point for semantic search
  lib/
    search_utils.py       paths + loaders (movies, stopwords)
    keyword_search.py     InvertedIndex: build/save/load, TF, IDF, BM25
    semantic_search.py    SemanticSearch: embeddings, vector math
  tests/                  pytest tests
cache/                    pickled index files (rebuilt by `build`, git-ignored)
data/                     movies.json + stopwords.txt (tracked inputs)
```

## Notes

- First `sentence-transformers` run downloads the `all-MiniLM-L6-v2` model (~90 MB) to
  `~/.cache/huggingface`. Expect a pause the first time; it is cached afterwards.
- The index is written to `cache/*.pkl`. If a command says "Index Not Found", run `build`.
- `cache/` is git-ignored because it is fully derived: `build` reproduces it byte-for-byte
  from `data/`. A fresh clone has the corpus but no index, so run `build` once after cloning.
- VS Code: Pylance is enabled, the interpreter is `.venv`, and `cli/` is an import root
  (see `.vscode/settings.json` and `pyrightconfig.json`). Debug configs are in
  `.vscode/launch.json`.
