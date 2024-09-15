from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry

# Define the Elasticsearch index for drugs
drug_index = Index('drugs')

# Define the Elasticsearch index for ICDs (or any other collection)
icd_index = Index('icds')

# --------------------------------------------------------
# Drug Document (For 'drugs_coll' collection)
# --------------------------------------------------------

@drug_index.document
class DrugDocument(Document):
    class Django:
        # The name of the MongoDB collection for drugs
        model = 'drugs_coll'

    class Index:
        # The name of the Elasticsearch index
        name = 'drugs'
        # Settings for the Elasticsearch index
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    # Fields that I want to index in Elasticsearch for the drugs collection
    brand_name = fields.TextField(attr='openfda.brand_name')
    generic_name = fields.TextField(attr='openfda.generic_name')
    manufacturer_name = fields.TextField(attr='openfda.manufacturer_name')

# --------------------------------------------------------
# ICD Document (For 'ICDs' collection)
# --------------------------------------------------------

@icd_index.document
class IcdDocument(Document):
    class Django:
        # The name of the MongoDB collection for ICDs
        model = 'ICDs'

    class Index:
        # The name of the Elasticsearch index for ICDs
        name = 'icds'
        # Settings for the Elasticsearch index
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }

    # Fields that I want to index in Elasticsearch for the ICDs collection
    icd_code = fields.TextField(attr='Code')
    title_en = fields.TextField(attr='Title_en')
    title_ar = fields.TextField(attr='Title_ar')
