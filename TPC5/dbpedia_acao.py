import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?filme ?label ?abstract
WHERE {
    ?filme a dbo:Film ;
        rdfs:label ?label ;
        dbo:abstract ?abstract ;
        dbo:wikiPageWikiLink dbr:Action_film .
    FILTER (LANG(?label) = 'en' && LANG(?abstract) = 'en') .
}
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
    filmes_acao = []
    for result in results["results"]["bindings"]:
        filmes_acao.append({
            "uri": result["filme"]["value"],
            "designacao": result["label"]["value"],
            "descricao": result["abstract"]["value"]
        })
    f = open("filmes_acao.json", "w")
    json.dump(filmes_acao, f)
    f.close()
else:
    print("Error:", response.status_code)
    print(response.text)
