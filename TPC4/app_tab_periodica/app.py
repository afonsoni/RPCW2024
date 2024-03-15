from flask import Flask, render_template, url_for
from datetime import datetime
import requests

app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/tabelaPeriodica"

@app.route('/')
def index():
    return render_template('index.html', data = { "data": data_hora_atual })

@app.route('/elementos')
def elements():
    # Send SPARQL query to GraphDB
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?na ?nome ?simb ?grupo_num ?grupo_nome where { 
	?s a tp:Element ;
        tp:name ?nome ;
        tp:symbol ?simb ;
        tp:atomicNumber ?na.
    ?s tp:group ?grupo .
    optional {?grupo tp:number ?grupo_num .}
    optional {?grupo tp:name ?grupo_nome .}
}  
order by ?na
"""
    payload = {"query": sparql_query}

    response = requests.get(graphdb_endpoint, params=payload,
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('elementos.html', data=data, time = data_hora_atual)
    else:
        return render_template('index.html', data= {"data": data_hora_atual})

@app.route('/elementos/<int:na>')
def element(na):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?na ?nome ?simb ?pa ?cor ?grupo_num ?grupo_nome ?period_num where {{ 
	?na a tp:Element ;  
        tp:atomicNumber {na} ;
        tp:name ?nome ;
    	tp:symbol ?simb ;
    	tp:atomicWeight ?pa ;
    	tp:color ?cor ;
        tp:group ?grupo ;
    	tp:period ?period .
    optional {{?grupo tp:number ?grupo_num .}}
    optional {{?grupo tp:name ?grupo_nome .}}
    ?period tp:number ?period_num .
    }}
"""
    payload = {"query": sparql_query}
    response = requests.get(graphdb_endpoint, params=payload,
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('elemento.html', data = data, num_atom = na, time = data_hora_atual)
    else:
        return render_template('empty.html', data=data)

@app.route('/grupos')
def grupos():
    sparql_query = """
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?grupo_num ?grupo_nome where {
		?s a tp:Group .
    	optional { ?s tp:number ?grupo_num .}
	    optional { ?s tp:name ?grupo_nome .}
    }
    order by ?grupo_num
    """
    payload = {"query": sparql_query}
    response = requests.get(graphdb_endpoint, params=payload,
        headers = {'Accept': 'application/sparql-results+json'}
    )
    if response.status_code == 200:
        data = response.json()['results']['bindings']
        return render_template('grupos.html', data = data, time = data_hora_atual)
    else: 
        return render_template('empty.html', data = {"data": data_hora_atual})

@app.route('/grupos/<int:grupo_num>')
def grupo_num(grupo_num):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?na ?nome ?simb ?pa ?cor ?period_num where {{ 
	?s a tp:Element ;  
        tp:atomicNumber ?na ;
        tp:name ?nome ;
        tp:symbol ?simb ;
        tp:atomicWeight ?pa ;
        tp:color ?cor ;
        tp:period ?period .
    ?period tp:number ?period_num .
    ?s tp:group ?g.
    ?g rdf:type tp:Group;
        tp:number "{grupo_num}"^^xsd:integer .
    }}
    """

    payload = { "query": sparql_query }

    response = requests.get(graphdb_endpoint, params = payload, headers = {"Accept": "application/sparql-results+json" })
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('grupo.html', data = data, grupo_id = grupo_num, time = data_hora_atual)
    else:
        return render_template('empty.html', data = data)
    
@app.route('/grupos/<string:grupo_nome>')
def grupo_nome(grupo_nome):
    sparql_query = f"""
    prefix tp: <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
    select ?na ?nome ?simb ?pa ?cor ?period_num where {{ 
	?s a tp:Element ;  
        tp:atomicNumber ?na ;
        tp:name ?nome ;
        tp:symbol ?simb ;
        tp:atomicWeight ?pa ;
        tp:color ?cor ;
        tp:period ?period .
    ?period tp:number ?period_num .
    ?s tp:group ?g.
    ?g rdf:type tp:Group;
        tp:name "{grupo_nome}" .
    }}
    """

    payload = { "query": sparql_query }

    response = requests.get(graphdb_endpoint, params = payload, headers = {"Accept": "application/sparql-results+json" })
    if response.status_code == 200:
        data = response.json()["results"]["bindings"]
        return render_template('grupo.html', data = data, grupo_id = grupo_nome, time = data_hora_atual)
    else:
        return render_template('empty.html', data = data)
    
if __name__ == '__main__':
    app.run(debug=True)