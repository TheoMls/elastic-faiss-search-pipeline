# Information Retrieval Class Project: Document Search & Indexing Pipeline

This repository contains the codebase for an Information Retrieval class project. The project explores two distinct search paradigms: lexical search using Elasticsearch (BM25) and dense semantic search using vector embeddings (FAISS).

## Dataset (IR2025)
The data used for this pipeline is provided as part of the **IR2025** dataset. Ensure the dataset folder (`IR2025/`) containing `documents.csv` and `queries.csv` is placed directly in the root directory of this project before running any scripts.

## Structure
- **`phase1/`**: Contains scripts and files for Lexical Search & Indexing (Elasticsearch via Docker).
- **`phase2/`**: Contains scripts, models, and results for Semantic Similarity Search (FAISS).

See the `README.md` in each phase's directory for specific instructions and details.

## Dependencies
Ensure you have the required libraries installed (can be found in `requirements.txt` files where applicable):
- `pandas`
- `numpy`
- `elasticsearch`
- `sentence-transformers`
- `faiss-cpu`
- `docker` (Required to run the local Elasticsearch instance)