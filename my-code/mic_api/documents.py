from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
import pymongo

# Define the Elasticsearch index
drug_index = Index('drugs')

@drug_index.document
class DrugDocument(Document):
    class Django:
        # The name of the MongoDB collection
        model = 'drugs_coll'

    class Index:
        name = 'drugs'
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    # Fields that i want to index in Elasticsearch
    brand_name = fields.TextField(attr='openfda.brand_name')
    generic_name = fields.TextField(attr='openfda.generic_name')



# # DISEASES DOCUMENTS
# # Define the Elasticsearch index
# diseases_index = Index('diseases_index')

# @diseases_index.document
# class DiseaseDocument(Document):
#     class Index:
#         name = 'diseases_index'
#         settings = {
#             "number_of_shards": 1,
#             "number_of_replicas": 0
#         }

#     # Fields to be indexed in Elasticsearch
#     code = fields.TextField()
#     title_en = fields.TextField()
#     title_ar = fields.TextField()
#     definition_en = fields.TextField()
#     definition_ar = fields.TextField()
#     index_terms_en = fields.TextField(multi=True)
#     index_terms_ar = fields.TextField(multi=True)

#     def get_queryset(self):
#         # Use MongoDB client to get data
#         client = pymongo.MongoClient("mongodb://localhost:27017/")
#         db = client['mic_db'] 
#         collection = db['diseases_coll']
#         return collection.find()  # This fetches all documents from the collection

#     def prepare_code(self, instance):
#         return instance.get('code', '')

#     def prepare_title_en(self, instance):
#         return instance.get('title', {}).get('en', '')

#     def prepare_title_ar(self, instance):
#         return instance.get('title', {}).get('ar', '')

#     def prepare_definition_en(self, instance):
#         return instance.get('definition', {}).get('en', '')

#     def prepare_definition_ar(self, instance):
#         return instance.get('definition', {}).get('ar', '')

#     def prepare_index_terms_en(self, instance):
#         return [term.get('label', {}).get('en', '') for term in instance.get('indexTerm', [])]

#     def prepare_index_terms_ar(self, instance):
#         return [term.get('label', {}).get('ar', '') for term in instance.get('indexTerm', [])]