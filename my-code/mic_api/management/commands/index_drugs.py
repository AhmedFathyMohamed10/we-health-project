import logging
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
from bson.objectid import ObjectId

MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'mic_db'
COLLECTION_NAME = 'icd_data'

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CHUNK_SIZE = 100

class Command(BaseCommand):
    help = 'Index drugs data into Elasticsearch'

    def handle(self, *args, **kwargs):
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        es = Elasticsearch()

        def convert_object_ids(doc):
            for key, value in doc.items():
                if isinstance(value, ObjectId):
                    doc[key] = str(value)
                elif isinstance(value, dict):
                    doc[key] = convert_object_ids(value)
                elif isinstance(value, list):
                    doc[key] = [convert_object_ids(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item for item in value]
            return doc

        def generate_data():
            for doc in collection.find():
                doc = convert_object_ids(doc)
                doc['disease_id'] = doc.pop('_id')
                yield {
                    "_index": "drugs",
                    "_source": doc
                }

        actions = list(generate_data())
        for i in range(0, len(actions), CHUNK_SIZE):
            chunk = actions[i:i + CHUNK_SIZE]
            try:
                helpers.bulk(es, chunk, request_timeout=60)
                self.stdout.write(self.style.SUCCESS(f'Indexed {i + len(chunk)} documents'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error indexing chunk {i // CHUNK_SIZE + 1}: {e}'))
                break

        self.stdout.write(self.style.SUCCESS('Data indexed successfully'))