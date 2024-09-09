import json
import os
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from django.conf import settings

class Command(BaseCommand):
    help = 'Load ICD data from JSON file into MongoDB'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing ICD data')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']

        # Read the JSON file
        try:
            with open(json_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error reading JSON file: {e}'))
            return

        # Connect to MongoDB
        try:
            client = MongoClient(settings.MONGO_URI)
            db = client.get_database('mic_db')
            collection = db['icd_data']
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error connecting to MongoDB: {e}'))
            return

        # Insert data into MongoDB
        try:
            if 'data' in data:
                collection.insert_many(data['data'])
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded data into MongoDB'))
            else:
                self.stderr.write(self.style.ERROR('No "data" key found in JSON file'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error inserting data into MongoDB: {e}'))
