# your_app/management/commands/load_json_to_mongo.py
import json
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Load JSON data into a MongoDB collection'

    def add_arguments(self, parser):
        # Command argument to pass the path to the JSON file
        parser.add_argument('json_file', type=str, help='The JSON file path')

    def handle(self, *args, **kwargs):
        json_file_path = kwargs['json_file']

        # Connect to MongoDB
        client = MongoClient(settings.MONGO_URI)
        db = client[settings.DB_NAME]

        # Specify the MongoDB collection
        collection = db['ICDs']

        # Check if the file exists
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'File "{json_file_path}" does not exist.'))
            return

        try:
            # Load the JSON file
            with open(json_file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

            if isinstance(data, list):  # If it's a list of documents
                # Insert multiple documents
                collection.insert_many(data)
            else:  # If it's a single document
                # Insert a single document
                collection.insert_one(data)

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded JSON data into MongoDB collection.'))

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format. Please check the JSON file.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
