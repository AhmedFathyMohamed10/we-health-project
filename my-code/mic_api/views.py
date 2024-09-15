# Imports
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient, IndexModel, TEXT
from pymongo.errors import PyMongoError
import logging
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from django.conf import settings

logger = logging.getLogger(__name__)


# MongoDB Configuration
MONGO_URI = settings.MONGO_URI
DB_NAME = settings.DB_NAME
COLLECTIONS = settings.COLLECTIONS 

DRUG_COLLECTION = COLLECTIONS[0]
ICD_COLLECTION = COLLECTIONS[1]

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
drug_collection = db[DRUG_COLLECTION]
icd_collection = db[ICD_COLLECTION]

# Drop existing indexes to avoid conflicts
drug_collection.drop_indexes()

# Create text search index for text searching 
indexes = [
    IndexModel([
        ('openfda.brand_name', TEXT),
        ('openfda.generic_name', TEXT),
    ], name='text_search_index'),
]
drug_collection.create_indexes(indexes)

# Elasticsearch client
es = Elasticsearch()


# --------------SEARCHING-----------------------------------------
def construct_query(search_terms, filters=None):
    should_clauses = []
    for term in search_terms:
        should_clauses.append({"match": {"brand_name": {"query": term, "fuzziness": "AUTO"}}})
        should_clauses.append({"match": {"generic_name": {"query": term, "fuzziness": "AUTO"}}})
    
    query = {
        "bool": {
            "should": should_clauses,
            "minimum_should_match": 1  # at least one should match
        }
    }

    if filters:
        filter_clauses = []
        for key, value in filters.items():
            filter_clauses.append({"term": {key: value}})
        
        query['bool']['filter'] = filter_clauses
    
    return query


PAGE_SIZE = 10
@api_view(['GET'])
def drug_search(request):
    try:
        search = request.GET.get('search', '')
        page = int(request.GET.get('page', 1))

        s = Search(using=es, index='drugs')
        if search:
            s = s.query("multi_match", query=search, fields=['openfda.brand_name', 'openfda.generic_name'], fuzziness='AUTO')

        total_count = s.count()
        start = (page - 1) * PAGE_SIZE
        s = s[start:start + PAGE_SIZE]
        response = s.execute()

        results = [hit.to_dict() for hit in response]
        total_pages = (total_count + PAGE_SIZE - 1) // PAGE_SIZE

        response_data = {
            'results': results,
            'total_count': total_count,
            'page': page,
            'total_pages': total_pages,
            'page_size': PAGE_SIZE
        }
        # print("Search query: %s", search)
        # print("Elasticsearch query: %s", s.to_dict())
        # print("Elasticsearch response: %s", response.to_dict())

        return Response(response_data)

    except Exception as e:
        logger.error("Error occurred during search: %s", e)
        return Response({'error': str(e)}, status=500)

# ---------------END OF SEARCHING --------------------------------

# -------------PRODUCT (DRUG) DETAILS-----------------------------
@api_view(['GET'])
def product_detail(request, set_id):
    try:
        product = drug_collection.find_one({'set_id': set_id}, {'_id': 0})
        if product:
            return Response(product)
        else:
            return Response({'error': 'Product not found'}, status=404)

    except PyMongoError as e:
        return Response({'error': str(e)}, status=500)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# ----------------------------------------------------------------

# -------------FILTERATIONS---------------------------------------
@api_view(['GET'])
def distinct_values(request):
    try:
        generic_names = drug_collection.distinct('openfda.generic_name')
        brand_names = drug_collection.distinct('openfda.brand_name')
        manufacturers = drug_collection.distinct('openfda.manufacturer_name')
        application_numbers = drug_collection.distinct('openfda.application_number')
        versions = drug_collection.distinct('version')

        response_data = {
            'generic_names': generic_names,
            'brand_names': brand_names,
            'manufacturers': manufacturers,
            'application_numbers': application_numbers,
            'versions': versions,
        }

        return Response(response_data)

    except PyMongoError as e:
        return Response({'error': str(e)}, status=500)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# -------------END OF FILTERATION----------------------------------

def fetch_interactions(drug_name, max_descriptions=3):
    logger.debug(f'Fetching interactions for: {drug_name}')
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"openfda.generic_name": drug_name}},
                    {"match": {"openfda.brand_name": drug_name}}
                ]
            }
        }
    }
    result = es.search(index="drugs", body=query)
    logger.debug(f'Elasticsearch result for {drug_name}: {result}')

    if not result['hits']['hits']:
        return [], f'{drug_name} not found in the database.'

    drug_doc = result['hits']['hits'][0]['_source']
    interactions_dict = {}  # Change from set to dict to hold descriptions

    if 'Rxdata' in drug_doc:
        rxdata_item = drug_doc['Rxdata']
        if rxdata_item and isinstance(rxdata_item, list) and len(rxdata_item) > 0:
            interactionTypeGroup = rxdata_item[0].get('interactionTypeGroup', [{}])
            if interactionTypeGroup and isinstance(interactionTypeGroup, list) and len(interactionTypeGroup) > 0:
                interactionType = interactionTypeGroup[0].get('interactionType', [{}])
                if interactionType and isinstance(interactionType, list) and len(interactionType) > 0:
                    interactionPair = interactionType[0].get('interactionPair', [])
                    if isinstance(interactionPair, list):
                        for interaction in interactionPair:
                            description = interaction.get('description', 'No description available')
                            interactionConcepts = interaction.get('interactionConcept', [])
                            if isinstance(interactionConcepts, list):
                                for concept in interactionConcepts:
                                    minConceptItem = concept.get('minConceptItem', {})
                                    if isinstance(minConceptItem, dict):
                                        min_name = minConceptItem.get('name', '').lower()
                                        if min_name:
                                            if min_name not in interactions_dict:
                                                interactions_dict[min_name] = set()  # Use set to avoid duplicates
                                            interactions_dict[min_name].add(description)  # Add description to the set
                                        else:
                                            logger.debug(f'Missing minConceptItem name in {concept}')
                                    else:
                                        logger.debug(f'Missing minConceptItem in {concept}')
                            else:
                                logger.debug(f'Expected list for interactionConcepts but got {type(interactionConcepts)}')
                else:
                    logger.debug('No valid interactionType found in interactionTypeGroup')
            else:
                logger.debug('No valid interactionTypeGroup found in Rxdata')
        else:
            logger.debug('No valid Rxdata found in drug_doc')
    else:
        logger.debug('No Rxdata found in drug_doc')

    # Convert dictionary to list of dictionaries with name and descriptions
    interactions_list = []
    for name, descriptions in interactions_dict.items():
        description_list = list(descriptions)
        interactions_list.append({
            'name': name,
            'descriptions': description_list[:max_descriptions],
            'more_descriptions_count': len(description_list) - max_descriptions if len(description_list) > max_descriptions else 0
        })
    
    logger.debug(f'Interactions for {drug_name}: {interactions_list}')
    return interactions_list, None

@api_view(['POST'])
def check_drug_interactions(request):
    try:
        drugs = [drug.strip().lower() for drug in request.data.get('drugs', [])]
        max_descriptions = int(request.data.get('max_descriptions', 10))

        if not drugs:
            return Response({'error': 'Please provide at least one drug.'}, status=400)

        interaction_details = []
        interaction_message = ''

        if len(drugs) == 1:
            drug1_interactions, message = fetch_interactions(drugs[0], max_descriptions)
            if message:
                return Response({'interactions': False, 'message': message})

            return Response({
                'interactions': True,
                'drug_interactions': drug1_interactions,
                'drug1_length': len(drug1_interactions),
                'message': f'{drugs[0]} interactions found. Total: {len(drug1_interactions)}.'
            })

        all_drug_interactions = {}
        for drug in drugs:
            drug_interactions, message = fetch_interactions(drug, max_descriptions)
            if message:
                interaction_message += message + ' '
            all_drug_interactions[drug] = drug_interactions

        for i, drug1 in enumerate(drugs):
            for drug2 in drugs[i + 1:]:
                drug1_interactions = all_drug_interactions.get(drug1, [])
                drug2_interactions = all_drug_interactions.get(drug2, [])

                if drug1_interactions and drug2_interactions:
                    for interaction in drug1_interactions:
                        if interaction['name'] == drug2:
                            for description in interaction['descriptions']:
                                interaction_details.append({
                                    'drug1': drug1,
                                    'drug2': drug2,
                                    'description': description
                                })
                    for interaction in drug2_interactions:
                        if interaction['name'] == drug1:
                            for description in interaction['descriptions']:
                                interaction_details.append({
                                    'drug1': drug2,
                                    'drug2': drug1,
                                    'description': description
                                })
                else:
                    logger.debug(f'No interactions found for {drug1} or {drug2}')

        if interaction_details:
            return Response({
                'interactions': True,
                'details': interaction_details,
                'message': 'Interactions found between the selected drugs.'
            })
        else:
            return Response({'interactions': False, 'message': interaction_message.strip() or 'No drug ⬌ drug interactions were found between the drugs in your list. However, this does not necessarily mean no drug interactions exist. Always consult your healthcare provider.'})

    except Exception as e:
        logger.error(f'Error checking drug interactions: {e}')
        return Response({'error': str(e)}, status=500)

# ----------------END OF DRUG ERUG INTERACTIONS --------------------

# -----------------------------------------------------------------
PAGE_SIZE = 5

@api_view(['GET'])
def disease_search(request):
    try:
        search_term = request.GET.get('search', '')
        icd_version = request.GET.get('icd_version', '').lower()  # '9', '10', or '11'
        page = int(request.GET.get('page', 1))

        icd_field_map = {
            '9': 'icd9Code.keyword',
            '10': 'icd10Code.keyword',
            '11': 'icd11Code.keyword'
        }
        icd_field = icd_field_map.get(icd_version)

        s = Search(using=es, index='icd_codes_index_02')

        query = []

        # Search by the selected ICD version if provided
        if icd_field and search_term:
            query.append({
                "terms": { 
                    icd_field: [search_term]
                }
            })

        # Search by title_en, title_ar, or index terms if provided
        if search_term:
            query.append({
                "multi_match": {
                    "query": search_term,
                    "fields": ['Title_en', 'Title_ar'],
                    "fuzziness": "AUTO"
                }
            })

        # Apply the query if any search criteria were provided
        if query:
            s = s.query("bool", should=query, minimum_should_match=1)

        # Collapse results by 'Code' to avoid duplicates
        s = s.extra(collapse={"field": "Code.keyword"})

        # Apply pagination
        start = (page - 1) * PAGE_SIZE
        s = s[start:start + PAGE_SIZE]

        # Execute search and get results
        logger.info(f"Search Query: {s.to_dict()}")  # Log the search query for debugging
        response = s.execute()
        results = [hit.to_dict() for hit in response]
        total_count = response.hits.total.value
        total_pages = (total_count + PAGE_SIZE - 1) // PAGE_SIZE

        # Construct response data
        response_data = {
            'results': results,
            'total_count': total_count,
            'page': page,
            'total_pages': total_pages,
            'page_size': PAGE_SIZE
        }

        return Response(response_data)

    except Exception as e:
        logger.error("Error occurred during search: %s", e)
        return Response({'error': str(e)}, status=500)

# --------------- END OF DISEASES API ------------------------------