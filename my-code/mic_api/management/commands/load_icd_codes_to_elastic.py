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
        mongo_collection = mongo_db['ICDs']  

        # Initialize Elasticsearch client
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        # Fetch all documents from MongoDB collection
        documents = list(mongo_collection.find({}))

        # Prepare bulk data for Elasticsearch
        actions = []
        for document in documents:
            # Fetch the fields that are lists (already lists in MongoDB)
            icd9Code = document.get("icd9Code", [])
            icd10Code = document.get("icd10Code", [])
            icd11Code = document.get("icd11Code", [])
            index_terms_en = document.get("IndexTerms_en", [])
            index_terms_ar = document.get("IndexTerms_ar", [])
            CombinedCodes = document.get("CombinedCodes", [])

            # Prepare the action for Elasticsearch bulk indexing
            action = {
                "_index": "icd_codes_index_05",  # Index name
                "_id": str(document.get("_id")),  
                "_source": {
                    "H1": document.get("H1"),
                    "H2": document.get("H2"),
                    "H3": document.get("H3"),
                    "H4": document.get("H4"),
                    "H5": document.get("H5"),
                    "Code": document.get("Code"),
                    "icd9Code": icd9Code,
                    "icd10Code": icd10Code,
                    "icd11Code": icd11Code,
                    "BlockLevel": document.get("BlockLevel"),
                    "Title_en": document.get("Title_en"),
                    "Title_ar": document.get("Title_ar"),
                    "Chapter": document.get("Chapter"),
                    "Definition_en": document.get("Definition_en"),
                    "Definition_ar": document.get("Definition_ar"),
                    "IndexTerms_en": index_terms_en,
                    "IndexTerms_ar": index_terms_ar,
                    "CombinedCodes": CombinedCodes,
                    "Inclusion": document.get("Inclusion"),
                    "Exclusion": document.get("Exclusion"),
                }
            }
            actions.append(action)

        # Bulk index documents to Elasticsearch
        if actions:
            helpers.bulk(es, actions)
            self.stdout.write(self.style.SUCCESS('Successfully indexed data into Elasticsearch'))
        else:
            self.stdout.write(self.style.WARNING('No documents found to index'))
