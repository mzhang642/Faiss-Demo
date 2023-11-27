from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import logging


# curl -X GET "http://localhost:9200/"
# index_name 's "description" is just a name for the Elasticsearch index
def initialize_elasticsearch(df, es_host, index_name="description"):
    try:
        es = Elasticsearch(hosts=[es_host])

        if es.indices.exists(index=index_name):
            es.indices.delete(index=index_name, ignore=[400, 404])

        mappings = {
            "mappings": {
                "properties": {
                    "description": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "brandOwner": {"type": "keyword"}  # This ensures that brandOwner is not analyzed
                }
            }
        }
        es.indices.create(index=index_name, body=mappings, ignore=400)
        

        # Fill NaN values with an empty string or appropriate default value
        docs = df.fillna('').to_dict(orient="records")

        bulk_payload = []

        for i, doc in enumerate(docs):
            bulk_payload.append({
                "_op_type": "index",
                "_index": index_name,
                "_id": i,
                "_source": {
                    "description": doc["description"],
                    "brandOwner": doc.get("brandOwner", "")
                }
            })
            if (i+1) % 10000 == 0:
                print(f"Processed {i+1} rows")

        # Execute the bulk index operation and capture the response
        success, failed = bulk(es, bulk_payload, index=index_name, raise_on_error=False, stats_only=False)
        if failed: 
            for failure in failed:
                logging.error(f"Failed document: {failure}")
        else:
            logging.info("Indexing complete. All documents indexed successfully.")
        return es
        
    
    except Exception as e:
        print(f"Failed to initialize Elasticsearch index: {e}")
        return None



def perform_fuzzy_search(es, query_data, index_name="description"):
    try:
         # Trim the query data to remove any potential whitespace
        query_data = query_data.strip()
        print(f"Searching for: {query_data}")  # Debugging log
        # Construct a multi_match query
        body = {
            "query": {
                "multi_match": {
                    "query": query_data,
                    "fields": ["description", "brandOwner"],
                    "type": "best_fields",
                    "tie_breaker": 0.3
                }
            }
        }
        results = es.search(index=index_name, body=body)
        food_matches = [
            {
                "name": hit['_source']['description'] + " - " + hit['_source']['brandOwner'], 
                "index": hit['_id']
            } 
            for hit in results['hits']['hits']
        ]
        return food_matches
    except Exception as e:
        logging.error(f"Error during Elasticsearch fuzzy search: {e}")
        return None
    

