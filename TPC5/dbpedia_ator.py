import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

ator_label = "Keanu Reeves"

# Define the SPARQL query
sparql_query = f"""
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?starring ?starringLabel ?filme ?label
WHERE {{
    ?filme a dbo:Film ;
        rdfs:label ?label ;
        dbo:starring ?starring .
    ?starring rdfs:label ?starringLabel .
    FILTER (LANG(?label) = 'en' && LANG(?starringLabel) = 'en' && regex(?starringLabel, "{ator_label}", "i")) .
}}
GROUP BY ?filme ?label
ORDER BY ?label
"""

# Define the headers
headers = {
    "Accept": "application/sparql-results+json"
}

# Define the parameters
params = {
    "query": sparql_query,
    "format": "json"
}

# Send the SPARQL query using requests
response = requests.get(sparql_endpoint, params=params, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    results = response.json()
    # Save the results to JSON
    filmes_ator = []
    for result in results["results"]["bindings"]:
        filmes_ator.append({
            "uri": result["filme"]["value"],
            "designacao": result["label"]["value"],
            "uri_atores": result["starring"]["value"],
            "atores": result["starringLabel"]["value"]
        })
    f = open("filmes_ator.json", "w")
    json.dump(filmes_ator, f)
    f.close()
else:
    print("Error:", response.status_code)
    print(response.text)
