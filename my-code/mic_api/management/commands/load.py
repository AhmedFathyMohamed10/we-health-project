from django.core.management.base import BaseCommand
import json
from pymongo import MongoClient
from bson import ObjectId
import os
from m_v_collection import MongoDBHandler as Handler

class Command(BaseCommand):
    help = 'Import data from JSON files into MongoDB'

    def handle(self, *args, **kwargs):
        client = MongoClient('mongodb://localhost:27017/')
        db = client['mic_db']
        collection = db['drugs_coll']

        input_dir = 'sample json outputs'
        try:
            for filename in os.listdir(input_dir):
                if filename.endswith('.json'):
                    file_path = os.path.join(input_dir, filename)
                    self._import_data_from_file(file_path, collection)

            self.stdout.write(self.style.SUCCESS('All data imported successfully'))
            # Categorize documents using MongoDBHandler
            mongo_handler = Handler()
            mongo_handler.categorize_documents()
        
        except:
            self.stdout.write(self.style.ERROR('Error importing main data'))

        finally:
            client.close()

    def _import_data_from_file(self, file_path, collection):
        with open(file_path, 'r') as f:
            data = json.load(f)

        try:
            # Transform `_id` fields if necessary
            for item in data:
                if '_id' in item and '$oid' in item['_id']:
                    item['_id'] = ObjectId(item['_id']['$oid'])

            # Insert data into MongoDB
            collection.insert_many(data)
            self.stdout.write(self.style.SUCCESS(f'Data from {file_path} imported successfully'))
        except:
            self.stdout.write(self.style.ERROR(f'Error importing data from {file_path}'))