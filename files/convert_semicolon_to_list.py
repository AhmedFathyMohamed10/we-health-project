import json

# Load the JSON file
with open('last_file.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Iterate over each item in the JSON and split the necessary fields
for item in data:
    # Convert 'IndexTerms_en' and 'IndexTerms_ar' into lists
    if item.get('IndexTerms_en'):
        item['IndexTerms_en'] = [term.strip() for term in item['IndexTerms_en'].split(';')]

    if item.get('IndexTerms_ar'):
        item['IndexTerms_ar'] = [term.strip() for term in item['IndexTerms_ar'].split(';')]

    # Convert 'icd9Code', 'icd10Code', and 'icd11Code' into lists
    if item.get('icd9Code'):
        item['icd9Code'] = [code.strip() for code in item['icd9Code'].split('&')]

    if item.get('icd10Code'):
        item['icd10Code'] = [code.strip() for code in item['icd10Code'].split('&')]

    if item.get('icd11Code'):
        # We assume icd11Code has no & separator, but if it does, handle it as well
        item['icd11Code'] = [code.strip() for code in item['icd11Code'].split('&')]

    if item.get('CombinedCodes'):
        # We assume icd11Code has no & separator, but if it does, handle it as well
        item['CombinedCodes'] = [code.strip() for code in item['CombinedCodes'].split('&')]

# Save the updated JSON back to a file
with open('icd.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("JSON has been successfully updated")
