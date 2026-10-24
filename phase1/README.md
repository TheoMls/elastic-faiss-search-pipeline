# Phase 1: Lexical Search & Indexing (Elasticsearch)

This phase prepares data and leverages Elasticsearch to perform traditional keyword-based retrieval.

## Files
*   **`csvToJsonl.py`:** Parses raw document data from a CSV file using `pandas` and restructures it into a JSON Lines (JSONL) format required for the Elasticsearch `_bulk` API. It prompts the user for the path to the CSV file and outputs `documents.jsonl`.
*   **`phase1.py`:** 
    *   Connects to a local Elasticsearch instance.
    *   Creates a new index (`ir2025`) configured with an `english` analyzer and `BM25` similarity.
    *   Ingests the JSONL documents using the Elasticsearch bulk helper.
    *   Reads user queries from a CSV, performs searches, and extracts the top $k$ results.
    *   Outputs results in either a readable standard text format or the official TREC evaluation format based on user input.

## How to Run

1.  **Start Elasticsearch:** Navigate to your `elastic-start-local` directory and execute the start script to spin up the local Docker-compose environment.
    ```bash
    cd elastic-start-local
    ./start.sh
    ```

2.  **Generate JSONL:** Run `python csvToJsonl.py`. When prompted, provide the path to your documents CSV file located in the root dataset folder (e.g., `../IR2025/documents.csv`) to generate the `documents.jsonl` file.

3.  **Run Search:** Run `python phase1.py` to index the documents and perform searches based on your queries CSV (e.g., `../IR2025/queries.csv`).

4.  **Stop Elasticsearch (Cleanup):** When you are finished, you can cleanly shut down the containers by running the stop script.
    ```bash
    cd elastic-start-local
    ./stop.sh
    ```