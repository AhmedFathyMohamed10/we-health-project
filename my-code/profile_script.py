from line_profiler import LineProfiler # type: ignore
import logging
logger = logging.getLogger(__name__)
def fetch_interactions(drug_doc):
    interactions_set = set()
    if 'Rxdata' in drug_doc:
        # Ensure 'Rxdata' has at least one item
        rxdata_item = drug_doc['Rxdata']
        if rxdata_item and isinstance(rxdata_item, list) and len(rxdata_item) > 0:
            interactionTypeGroup = rxdata_item[0].get('interactionTypeGroup', [{}])
            
            # Ensure 'interactionTypeGroup' has at least one item
            if interactionTypeGroup and isinstance(interactionTypeGroup, list) and len(interactionTypeGroup) > 0:
                interactionType = interactionTypeGroup[0].get('interactionType', [{}])
                
                # Ensure 'interactionType' has at least one item
                if interactionType and isinstance(interactionType, list) and len(interactionType) > 0:
                    interactionPair = interactionType[0].get('interactionPair', [])
                    
                    # Ensure 'interactionPair' is a list
                    if isinstance(interactionPair, list):
                        for interaction in interactionPair:
                            description = interaction.get('description', 'No description available')
                            interactionConcepts = interaction.get('interactionConcept', [])
                            
                            # Ensure 'interactionConcept' is a list and has at least 2 items
                            if isinstance(interactionConcepts, list) and len(interactionConcepts) > 1:
                                # Access the second item
                                concept = interactionConcepts[1]
                                minConceptItem = concept.get('minConceptItem', {})
                                sourceConceptItem = concept.get('sourceConceptItem', {})
                                
                                # Extract and log the minConceptItem details
                                if isinstance(minConceptItem, dict):
                                    min_name = minConceptItem.get('name', '').lower()
                                    if min_name:
                                        interactions_set.add((min_name, description))
                                    else:
                                        logger.debug(f'Missing minConceptItem name in {concept}')
                                else:
                                    logger.debug(f'Missing minConceptItem in {concept}')
                            else:
                                logger.debug(f'Expected list for interactionConcepts with at least 2 items but got {len(interactionConcepts)}')
                else:
                    logger.debug('No valid interactionType found in interactionTypeGroup')
            else:
                logger.debug('No valid interactionTypeGroup found in Rxdata')
        else:
            logger.debug('No valid Rxdata found in drug_doc')
    else:
        logger.debug('No Rxdata found in drug_doc')
    return interactions_set

# Example drug_doc
drug_doc = {
    "Rxdata": [
        {
            "nlmDisclaimer": "It is not the intention of NLM to provide specific medical advice, but rather to provide users with information to better understand their health and their medications. NLM urges you to consult with a qualified physician for advice about medications.",
            "interactionTypeGroup": [
                {
                    "sourceDisclaimer": "DrugBank is intended for educational and scientific research purposes only and you expressly acknowledge and agree that use of DrugBank is at your sole risk. The accuracy of DrugBank information is not guaranteed and reliance on DrugBank shall be at your sole risk. DrugBank is not intended as a substitute for professional medical advice, diagnosis or treatment..[www.drugbank.ca]",
                    "sourceName": "DrugBank",
                    "interactionType": [
                        {
                            "comment": "nicotine 4 MG Chewing Gum (311975) is resolved to nicotine polacrilex (31765)",
                            "minConceptItem": {
                                "rxcui": "311975",
                                "name": "nicotine 4 MG Chewing Gum",
                                "tty": "SCD"
                            },
                            "interactionPair": [
                                {
                                    "interactionConcept": [
                                        {
                                            "minConceptItem": {
                                                "rxcui": "31765",
                                                "name": "nicotine polacrilex",
                                                "tty": "PIN"
                                            },
                                            "sourceConceptItem": {
                                                "id": "DB00184",
                                                "name": "Nicotine",
                                                "url": "https://go.drugbank.com/drugs/DB00184#interactions"
                                            }
                                        },
                                        {
                                            "minConceptItem": {
                                                "rxcui": "1000581",
                                                "name": "trichlorfon",
                                                "tty": "IN"
                                            },
                                            "sourceConceptItem": {
                                                "id": "DB11473",
                                                "name": "Metrifonate",
                                                "url": "https://go.drugbank.com/drugs/DB11473#interactions"
                                            }
                                        }
                                    ],
                                    "severity": "N/A",
                                    "description": "The risk or severity of adverse effects can be increased when Metrifonate is combined with Nicotine."
                                },
                                {
                                    "interactionConcept": [
                                        {
                                            "minConceptItem": {
                                                "rxcui": "31765",
                                                "name": "nicotine polacrilex",
                                                "tty": "PIN"
                                            },
                                            "sourceConceptItem": {
                                                "id": "DB00184",
                                                "name": "Nicotine",
                                                "url": "https://go.drugbank.com/drugs/DB00184#interactions"
                                            }
                                        },
                                        {
                                            "minConceptItem": {
                                                "rxcui": "1001",
                                                "name": "antipyrine",
                                                "tty": "IN"
                                            },
                                            "sourceConceptItem": {
                                                "id": "DB01435",
                                                "name": "Antipyrine",
                                                "url": "https://go.drugbank.com/drugs/DB01435#interactions"
                                            }
                                        }
                                    ],
                                    "severity": "N/A",
                                    "description": "The metabolism of Antipyrine can be decreased when combined with Nicotine."
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}

import pprint

def main():
    interactions = fetch_interactions(drug_doc)
    printer = pprint.PrettyPrinter(indent=4)
    printer.pprint(interactions)

if __name__ == "__main__":
    profiler = LineProfiler(fetch_interactions)
    profiler.run('main()')
    profiler.print_stats()
