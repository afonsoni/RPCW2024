import requests
import json

# Define the DBpedia SPARQL endpoint
sparql_endpoint = "http://dbpedia.org/sparql"

# Define the SPARQL query
sparql_query = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?filme ?label
        (GROUP_CONCAT(DISTINCT ?directorLabel; SEPARATOR=", ") AS ?directorLabels)
        (GROUP_CONCAT(DISTINCT ?starringLabel; SEPARATOR=", ") AS ?starringLabels)
        (GROUP_CONCAT(DISTINCT ?writerLabel; SEPARATOR=", ") AS ?writerLabels)
        (GROUP_CONCAT(DISTINCT ?musicComposerLabel; SEPARATOR=", ") AS ?musicComposerLabels)
        (GROUP_CONCAT(DISTINCT ?cinematographyLabel; SEPARATOR=", ") AS ?cinematographyLabels)
WHERE {
    ?filme a dbo:Film ;
        rdfs:label ?label ;
        dbo:runtime ?runtime .
OPTIONAL { ?filme dbo:director ?director .
            ?director rdfs:label ?directorLabel .
            FILTER (LANG(?directorLabel) = 'en') }
OPTIONAL { ?filme dbo:starring ?starring .
            ?starring rdfs:label ?starringLabel .
            FILTER (LANG(?starringLabel) = 'en') }
OPTIONAL { ?filme dbo:writer ?writer .
            ?writer rdfs:label ?writerLabel .
            FILTER (LANG(?writerLabel) = 'en') }
OPTIONAL { ?filme dbo:musicComposer ?musicComposer .
            ?musicComposer rdfs:label ?musicComposerLabel .
            FILTER (LANG(?musicComposerLabel) = 'en') }
OPTIONAL { ?filme dbo:cinematography ?cinematography .
            ?cinematography rdfs:label ?cinematographyLabel .
            FILTER (LANG(?cinematographyLabel) = 'en') }
    FILTER (LANG(?label) = 'en' && ?runtime <= 2400) .
}
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
    filmes_curta = []
    for result in results["results"]["bindings"]:
        filmes_curta.append({
            "uri": result["filme"]["value"],
            "designacao": result["label"]["value"],
            "ator(es)": result["starringLabels"]["value"],
            "realizador": result["directorLabels"]["value"],
            "escritor": result["writerLabels"]["value"],
            "musico": result["musicComposerLabels"]["value"],
            "cinematografia": result["cinematographyLabels"]["value"]
        })
    f = open("filmes_curta.json", "w")
    json.dump(filmes_curta, f)
    f.close()
else:
    print("Error:", response.status_code)
    print(response.text)
