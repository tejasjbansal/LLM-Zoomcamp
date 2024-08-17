from elasticsearch import Elasticsearch
import json
from typing import List, Dict, Union
import numpy as np

@data_exporter
def elasticsearch(documents: List[Dict[str, Union[Dict, List[int], str]]], *args, **kwargs):
    connection_string = kwargs.get('connection_string', 'http://elasticsearch:9200')
    index_name = kwargs.get('index_name', 'documents')
    number_of_shards = kwargs.get('number_of_shards', 1)
    number_of_replicas = kwargs.get('number_of_replicas', 0)
    dimensions = kwargs.get('dimensions')

    if dimensions is None and len(documents) > 0:
        document = documents[0]
        dimensions = len(document.get('embedding') or [])

    # Increase timeout settings
    es_client = Elasticsearch(connection_string, timeout=60, max_retries=3, retry_on_timeout=True)
    
    # Check if Elasticsearch is reachable
    try:
        es_info = es_client.info().body
        print(f'Successfully connected to Elasticsearch at {connection_string}')
        print(json.dumps(es_info, indent=2))
    except Exception as e:
        print(f'Error connecting to Elasticsearch at {connection_string}: {e}')
        return

    index_settings = {
        "settings": {
            "number_of_shards": number_of_shards,
            "number_of_replicas": number_of_replicas,
        },
        "mappings": {
            "properties": {
                "chunk": {"type": "text"},
                "document_id": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": dimensions}
            }
        }
    }

    # Recreate the index by deleting if it exists and then creating with new settings
    try:
        if es_client.indices.exists(index=index_name).body:
            es_client.indices.delete(index=index_name)
            print(f'Index {index_name} deleted')

        es_client.indices.create(index=index_name, body=index_settings)
        print('Index created with properties:')
        print(json.dumps(index_settings, indent=2))
        print('Embedding dimensions:', dimensions)
    except Exception as e:
        print(f'Error creating index {index_name}: {e}')
        return

    count = len(documents)
    print(f'Indexing {count} documents to Elasticsearch index {index_name}')
    for idx, document in enumerate(documents):
        if idx % 100 == 0:
            print(f'{idx + 1}/{count}')

        if isinstance(document['embedding'], np.ndarray):
            document['embedding'] = document['embedding'].tolist()

        try:
            es_client.index(index=index_name, document=document)
        except Exception as e:
            print(f'Error indexing document {idx}: {e}')

    return [[d['embedding'] for d in documents[:10]]]
