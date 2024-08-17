if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from typing import Dict, List, Union

import numpy as np
from elasticsearch import Elasticsearch, exceptions


@data_loader
def search(*args, **kwargs) -> List[Dict]:
    """
    query_embedding: Union[List[int], np.ndarray]
    """
    
    connection_string = kwargs.get('connection_string', 'http://elasticsearch:9200')
    # index_name = kwargs.get('index_name', 'documents')
    index_name = 'llm_documents_20240817_0959'
    es_client = Elasticsearch(connection_string)
    query = "When is the next cohort?"

    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^4", "text"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }
    response = es_client.search(index=index_name,body=search_query)
    print(response)
    result_docs = []
    
    for hit in response['hits']['hits']:
        result_docs.append(hit['_score'])

    return result_docs
    
    

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'