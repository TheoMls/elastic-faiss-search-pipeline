# get necessary libraries by: pip install -r requirements.txt
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import faiss
import pickle
import os

def main():
    #1
    # load data from csv
    df = pd.read_csv("IR2025\\documents.csv")
    doc_ids = df["ID"].tolist()
    doc_text = df["Text"].tolist()
    print("loaded data")

    df = pd.read_csv("IR2025\\queries.csv")
    query_ids = df["ID"].tolist()
    query_text = df["Text"].tolist()
    print("loaded queries")

    #2
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # using pretraind model to generate data embeddings or get them from pickle
    if os.path.exists("data_embeddings.pkl"):
        print("using pickle to load embeddings")
        with open("data_embeddings.pkl", "rb") as results_file:
            text_embeddings = pickle.load(results_file)
    else:
        print("using model to generate embeddings")
        text_embeddings = model.encode(doc_text, show_progress_bar=True)

        # store embeddings 
        with open("data_embeddings.pkl", "wb") as results_file:
            pickle.dump(text_embeddings, results_file)
            
    # using pretraind model to generate query embeddings or get them from pickle
    if os.path.exists("query_embeddings.pkl"):
        print("using pickle to load queries")
        with open("query_embeddings.pkl", "rb") as results_file:
            query_embeddings = pickle.load(results_file)
    else:
        print("using model to generate queries")
        query_embeddings = model.encode(query_text, show_progress_bar=True)

        # store embeddings 
        with open("query_embeddings.pkl", "wb") as results_file:
            pickle.dump(query_embeddings, results_file)

    #3
    # normalize embeddings for inner product similarity
    faiss.normalize_L2(text_embeddings)
    faiss.normalize_L2(query_embeddings)

    # build faiss index
    dimension = text_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(text_embeddings)
    print("built faiss index")

    #4
    # perform search
    k_values = [20, 30, 50]
    for k in k_values:
        distances, indices = index.search(query_embeddings, k)
        print(f"performed search for k={k}")
        # save results to file
        results_file = open(os.path.join(os.getcwd(), 'phase2', 'top_k_query_results', f'results_k{k}.txt'), 'w', encoding="utf-8")
        for q_idx, query_id in enumerate(query_ids):
            for rank, doc_idx in enumerate(indices[q_idx]):
                doc_id = doc_ids[doc_idx]
                score = distances[q_idx][rank]
                results_file.write(f"{query_id} Q0 {doc_id} {rank+1} {score} k{k}\n")
        results_file.close()
        print(f"saved results for k={k}")


if __name__ == "__main__":
    main()