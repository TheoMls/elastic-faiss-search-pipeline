import os
import json
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers

#connecting client with elastic search
#for runnig with elastic-start-local with api key on enviroment variables
print("Conecting...")
client = Elasticsearch(
    "http://localhost:9200",
    api_key = os.getenv("ELASTIC_API_KEY"),
    request_timeout = 30
)
print("Connected")

index_name = 'ir2025'
def create_ir2025_index(): 
    #creating the index in elastic search
    if client.indices.exists(index=index_name):
        print("Deleting preexistent index...")
        client.indices.delete(index=index_name)

    index_mapping_parametres = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "english_analyzer": {
                        "type": "english"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": { "type": "keyword" },
                "text": {
                    "type": "text",
                    "analyzer": "english_analyzer",
                    "similarity": "BM25"
                }
            }
        }
    }

    print("Creating index...")
    client.indices.create(index=index_name)
    print("Index created")

    #using bulk helpers to populate the index
    #generator that yields the data that bulk needs to populate the index
    def generate_data(jsonl_file):
        with open(jsonl_file, 'r', encoding="utf-8") as data_file:
            while True:
                index_line = data_file.readline()
                data_line = data_file.readline()
                if not index_line or not data_line:
                    break;

                index = json.loads(index_line)
                data = json.loads(data_line)
                yield {
                    "_index": index_name,
                    "_id": data["id"],
                    "_source": data
                }

    print("Uploading data...")
    success, errors = helpers.bulk(client,generate_data(os.path.join(os.getcwd(), 'phase1', 'documents.jsonl')),
                                   raise_on_error=False
                                )
    print("Data uploaded")
    print(f"Total documents successfully uploaded: {success}")
    print(f"Total failed documents: {len(errors)}")

create_ir2025_index()

#read queries from csv, use them to search the data with elastic search and save the results on relative .txt file
fileDir = input("give queries csv file dir: ")
df = pd.read_csv(fileDir, encoding="utf-8")

def get_top_k_query_results(k, treq_eval_form):
    #file to save results
    s = '' if treq_eval_form == False else '_trec_eval_form' #s is used in file name to specify if it is in treq_eval_form
    results_file = open(os.path.join(os.getcwd(), 'phase1', 'top_k_query_results', f'results_k{k}{s}.txt'), 'w', encoding="utf-8")

    #read each queue, get results from elastic search and write them on results.txt
    for index, row in df.iterrows():
        id = row["ID"]
        print(f'Searching for query: {id}')
        text = str(row["Text"])

        resp = client.search(
            index = index_name,
            size = k,
            query={ 'match': { 'text': text } }
        )
        #write results in results_file
        results = resp["hits"]["hits"]
        if treq_eval_form == False: #write data in file regulary
            results_file.write(f'----------------------------------------------------------------------------------------------------\nQuery: {id}\n')
            for item in results:
                results_file.write(f'id: {item["_id"]} score: {item["_score"]}\ndata: {item["_source"]["text"]}\n')
        else: #write data in treq_eval_form
            rank = 1
            for item in results:
                results_file.write(f'{id} Q0 {item["_id"]} {rank} {item["_score"]} k{k}\n')
                rank = rank + 1
    print(f'Created results_k{k}{s}.txt')
    results_file.close()


#get k values from user and for each one if we want the relative file to be in treq_eval_form or not

k_values_treq_eval_form = []
print("k Values for treq_eval_form")
print("Give k value (-1 to stop)")
k = input(f'Value {len(k_values_treq_eval_form)+1}: ')
while int(k) > 0:
    k_values_treq_eval_form.append(k)
    k = input(f'Value {len(k_values_treq_eval_form)+1}: ')

k_values = []
print("k Values for regular form")
print("Give k value (-1 to stop)")
k = input(f'Value {len(k_values)+1}: ')
while int(k) > 0:
    k_values.append(k)
    k = input(f'Value {len(k_values)+1}: ')

for k in k_values_treq_eval_form:
    print(f'---------- Getting results for k = {k} with treq_eval_form ----------')
    get_top_k_query_results(k, True)

for k in k_values:
    print(f'---------- Getting results for k = {k} without treq_eval_form ----------')
    get_top_k_query_results(k, False)