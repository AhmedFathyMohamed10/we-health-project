from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
from bson import ObjectId 


# MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['mic_db']
collection = db['drugs_coll']


# Elasticsearch client
es = Elasticsearch('http://localhost:9200')

# Elasticsearch index name
ELASTICSEARCH_INDEX = 'drugs_index_test'

# Fetch documents from MongoDB
documents = collection.find()

# Function to convert ObjectId to string
def convert_objectid_to_str(document):
    for key, value in document.items():
        if isinstance(value, ObjectId):
            document[key] = str(value)
        elif isinstance(value, dict):
            convert_objectid_to_str(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    convert_objectid_to_str(item)

# Index documents in Elasticsearch
actions = []
for doc in documents:
    convert_objectid_to_str(doc)
    actions.append({
        "_index": ELASTICSEARCH_INDEX,
        "_id": str(doc["_id"]),
        "_source": doc
    })

helpers.bulk(es, actions)
print(f"Indexed {len(actions)} documents into Elasticsearch index '{ELASTICSEARCH_INDEX}'.")
