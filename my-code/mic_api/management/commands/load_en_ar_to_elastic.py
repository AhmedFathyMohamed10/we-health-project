from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch, helpers
import json
import os

class Command(BaseCommand):
    help = 'Load data into Elasticsearch'

    def handle(self, *args, **kwargs):
        es = Elasticsearch()

        base_dir = os.path.dirname(os.path.abspath(__file__))
        manage_py_dir = os.path.abspath(os.path.join(base_dir, '../../../'))

        english_file = os.path.join(manage_py_dir, 'cleaned_icd_results_en.json')
        arabic_file = os.path.join(manage_py_dir, 'icd-results_ar.json')

        def load_data_to_es(english_file, arabic_file, index_name):
            with open(english_file, 'r', encoding='utf-8') as eng_file, open(arabic_file, 'r', encoding='utf-8') as ara_file:
                eng_data = json.load(eng_file)['data']  # Access the 'data' key
                ara_data = json.load(ara_file)['data']  # Access the 'data' key
                
                # Create a dictionary for quick lookup by code
                ara_dict = {entry['code']: entry for entry in ara_data}

                actions = []

                for eng_entry in eng_data:
                    code = eng_entry.get('code')
                    if not code:
                        continue

                    # Lookup the corresponding Arabic entry
                    ara_entry = ara_dict.get(code, {})

                    # Safely access nested fields with default values
                    title_en = eng_entry.get('title', {}).get('@value', '')
                    definition_en = eng_entry.get('definition', {}).get('@value', '') if eng_entry.get('definition') else ''
                    index_terms_en = [term.get('label', {}).get('@value', '') for term in (eng_entry.get('indexTerm') or [])]

                    title_ar = ara_entry.get('title', {}).get('@value', '')
                    definition_ar = ara_entry.get('definition', {}).get('@value', '') if ara_entry.get('definition') else ''
                    index_terms_ar = [term.get('label', {}).get('@value', '') for term in (ara_entry.get('indexTerm') or [])]

                    document = {
                        "_index": index_name,
                        "_source": {
                            "code": code,
                            "title_en": title_en,
                            "title_ar": title_ar,
                            "definition_en": definition_en,
                            "definition_ar": definition_ar,
                            "index_terms_en": index_terms_en,
                            "index_terms_ar": index_terms_ar
                        }
                    }

                    actions.append(document)

                helpers.bulk(es, actions)

        # Load data
        load_data_to_es(english_file, arabic_file, 'diseases_index')
