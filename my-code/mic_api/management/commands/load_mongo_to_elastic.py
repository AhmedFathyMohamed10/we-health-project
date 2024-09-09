# from django.core.management.base import BaseCommand
# from mic_api.documents import DiseaseDocument
# import pymongo

# class Command(BaseCommand):
#     help = 'Load data from MongoDB to Elasticsearch'

#     def handle(self, *args, **kwargs):
#         client = pymongo.MongoClient("mongodb://localhost:27017/")
#         db = client['mic_db']  
#         collection = db['diseases_coll']  

#         # Fetch all documents from MongoDB
#         documents = collection.find()

#         # Index documents into Elasticsearch
#         for doc in documents:
#             DiseaseDocument().update_or_create(
#                 id=doc.get('code'),  # Assuming 'code' is unique
#                 defaults={
#                     'code': doc.get('code', ''),
#                     'title_en': doc.get('title_en', ''),
#                     'title_ar': doc.get('title_ar', ''),
#                     'definition_en': doc.get('definition_en', ''),
#                     'definition_ar': doc.get('definition_ar', ''),
#                     'index_terms_en': doc.get('index_terms_en', []),
#                     'index_terms_ar': doc.get('index_terms_ar', [])
#                 }
#             )