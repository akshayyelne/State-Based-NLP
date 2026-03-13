import re

def extract_entities(text):
    entities = {}

    policy_match = re.search(r'\bP\d{5,}\b', text)
    if policy_match:
        entities["policy_number"] = policy_match.group()

    claim_match = re.search(r'\bCLM\d{4,}\b', text)
    if claim_match:
        entities["claim_id"] = claim_match.group()

    # Support both DD/MM/YYYY and YYYY-MM-DD
    date_match = re.search(r'\b\d{2}/\d{2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b', text)
    if date_match:
        entities["incident_date"] = date_match.group()

    return entities


