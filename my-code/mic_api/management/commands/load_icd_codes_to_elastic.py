import json
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers

class Command(BaseCommand):
    help = 'Index ICD codes from MongoDB into Elasticsearch'

    def handle(self, *args, **kwargs):
        # Initialize MongoDB client and connect to the database
        mongo_client = MongoClient('mongodb://localhost:27017/')
        mongo_db = mongo_client['mic_db']
        mongo_collection = mongo_db['icd_data']  

        # Initialize Elasticsearch client
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        # Fetch all documents from MongoDB collection
        documents = list(mongo_collection.find({}))

        # Prepare bulk data for Elasticsearch
        actions = []
        for document in documents:
            action = {
                "_index": "icd_codes_index",  
                "_id": str(document.get("_id")),
                "_source": {
                    "icd9Code": document.get("icd9Code"),
                    "icd10Code": document.get("icd10Code"),
                    "icd11Code": document.get("icd11Code"),
                    "Code": document.get("Code"),
                    "Title_en": document.get("Title_en"),
                    "Title_ar": document.get("Title_ar"),
                    "Inclusion": document.get("Inclusion"),
                    "Exclusion": document.get("Exclusion"),
                    "IndexTerms_en": document.get("IndexTerms_en"),
                    "IndexTerms_ar": document.get("IndexTerms_ar"),
                }
            }
            actions.append(action)

        # Bulk index documents to Elasticsearch
        if actions:
            helpers.bulk(es, actions)
            self.stdout.write(self.style.SUCCESS('Successfully indexed data into Elasticsearch'))
        else:
            self.stdout.write(self.style.WARNING('No documents found to index'))
