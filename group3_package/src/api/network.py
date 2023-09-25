import requests
import json

def extract_protein_sequence_from_json(data):
    query_results = data['results']
    if len(query_results) > 0:
        first_query_result = query_results[0]
        hits = first_query_result['hits']
        if len(hits) > 0:
            first_hit = hits[0]
            return first_hit['protein_sequence']
    return None



url = "https://example.com/api/blast"
sequence = "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPVAGVANALAHKYH"
params = {
    "sequence": sequence,
    "format": "json",
    "search_type": "blastp",
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = json.loads(response.text)
    protein_sequence = extract_protein_sequence_from_json(data)
    print(protein_sequence)
else:
    print("Request failed with status code:", response.status_code)



