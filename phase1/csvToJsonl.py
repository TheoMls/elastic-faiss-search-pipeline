import os
import pandas as pd
import json

fileDir = input("give csv file dir: ")

df = pd.read_csv(fileDir, encoding="utf-8")

with open(os.path.join(os.getcwd(), 'phase1', 'documents.jsonl'), 'w', encoding="utf-8") as jsonl_file:
    for index, row in df.iterrows():
        id = int(row["ID"])
        text = str(row["Text"])
        index_row = { "index": { "_id": id } }
        data_row = { "id": id, "text": text }
        
        jsonl_file.write(json.dumps(index_row) + "\n")
        jsonl_file.write(json.dumps(data_row) + "\n")

jsonl_file.close()