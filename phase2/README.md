# Phase 2: Semantic Similarity Search (FAISS)

This phase implements a dense retrieval system using transformer models and a vector database to capture semantic meaning.

## Files
*   **`phase2.py`:** The main script for generating embeddings and performing the vector search.
*   **`requirements.txt`:** Lists the required Python packages (`pandas`, `numpy`, `faiss-cpu`, `sentence-transformers`).
*   **`top_k_query_results/`**: Directory containing the output files with the top $k$ results for each query in standard TREC format.

## Process Details
1.  **Vectorization:** Uses the `sentence-transformers` library (e.g., `all-MiniLM-L6-v2`) to encode text documents and search queries into dense vector embeddings.
2.  **Caching:** Caches the generated embeddings locally via `pickle` (`data_embeddings.pkl`, `query_embeddings.pkl`) to accelerate subsequent runs and avoid re-computing embeddings.
3.  **Vector Indexing & Search:** Normalizes the embeddings (L2) and constructs a FAISS `IndexFlatIP` (Inner Product) index for efficient nearest-neighbor search.
4.  **Output:** Retrieves the top $k$ relevant documents ($k=20, 30, 50$) for each query and exports the rankings in standard TREC evaluation format to the `top_k_query_results` folder.

## How to Run

1.  **Install Requirements:** Make sure your environment is set up by running:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Check Dataset:** Ensure the `IR2025/` folder containing `documents.csv` and `queries.csv` is securely located at the project root directory.
3.  **Run Semantic Search:** Execute the main script:
    ```bash
    python phase2.py
    ```