import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

film_label = "The Matrix"

# Define the SPARQL query
sparql_query = f"""
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?filme ?label
        (GROUP_CONCAT(DISTINCT ?starring; SEPARATOR=", ") AS ?starringList)
        (GROUP_CONCAT(DISTINCT ?starringLabel; SEPARATOR=", ") AS ?starringLabels)
WHERE {{
    ?filme a dbo:Film ;
        rdfs:label ?label ;
        dbo:starring ?starring .
    ?starring rdfs:label ?starringLabel .
    FILTER (LANG(?label) = 'en' && LANG(?starringLabel) = 'en' && regex(?label, "{film_label}", "i")) .
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
    filmes_elenco = []
    for result in results["results"]["bindings"]:
        filmes_elenco.append({
            "uri": result["filme"]["value"],
            "designacao": result["label"]["value"],
            "uri_atores": result["starringList"]["value"],
            "atores": result["starringLabels"]["value"]
        })
    f = open("filmes_elenco.json", "w")
    json.dump(filmes_elenco, f)
    f.close()
else:
    print("Error:", response.status_code)
    print(response.text)
