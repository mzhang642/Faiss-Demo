from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging


# curl -X GET "http://localhost:9200/"
def initialize_elasticsearch(df, es_host, index_name="description"):
    try:
        es = Elasticsearch(hosts=[es_host])

        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name, ignore=[400, 404])

        es.indices.create(index=index_name, ignore=400)

        docs = df.to_dict(orient="records")
        bulk_payload = []

        for i, doc in enumerate(docs):
            bulk_payload.append({
                "_op_type": "index",
                "_index": index_name,
                "_id": i,
                "_source": {
                    "description": doc["description"]
                }
            })
            if (i+1) % 10000 == 0:
                print(f"Processed {i+1} rows")

        bulk(es, bulk_payload)
        print("Indexing complete")

        return es
    except Exception as e:
        print(f"Failed to initialize Elasticsearch index: {e}")
        return None



def perform_fuzzy_search(es, query_data, index_name="description"):
    try:
        results = es.search(index=index_name, body={
            "query": {
                "fuzzy": {
                    "description": query_data
                }
            }
        })
        food_matches = [{"name": hit['_source']['description'], "index": hit['_id']} for hit in results['hits']['hits']]
        return food_matches
    except Exception as e:
        logging.error(f"Error during Elasticsearch fuzzy search: {e}")
        return None
    

