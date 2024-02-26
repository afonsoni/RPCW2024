import json

with open("escolaMusica.json", encoding="utf-8") as f:
    try:
        bd = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        raise

ttl = """@prefix : <http://rpcw.di.uminho.pt/2024/musica/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/2024/musica/> .

<http://rpcw.di.uminho.pt/2024/musica> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#ensinaIntrumento
:ensinaIntrumento rdf:type owl:ObjectProperty ;
                    rdfs:domain :Curso ;
                    rdfs:range :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#temCurso
:temCurso rdf:type owl:ObjectProperty ;
            rdfs:domain :Aluno ;
            rdfs:range :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#temInstrumento
:temInstrumento rdf:type owl:ObjectProperty ;
                rdfs:domain :Aluno ;
                rdfs:range :Instrumento .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#anoCurso
:anoCurso rdf:type owl:DatatypeProperty ;
            rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/musica#dataNasc
:dataNasc rdf:type owl:DatatypeProperty ;
            rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/musica#designacao
:designacao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#duracao
:duracao rdf:type owl:DatatypeProperty ;
            rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#idAluno
:idAluno rdf:type owl:DatatypeProperty ;
            rdfs:domain :Aluno .


###  http://rpcw.di.uminho.pt/2024/musica#idCurso
:idCurso rdf:type owl:DatatypeProperty ;
            rdfs:domain :Curso .


###  http://rpcw.di.uminho.pt/2024/musica#idInstrumento
:idInstrumento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#instrumento
:instrumento rdf:type owl:DatatypeProperty ;
                rdfs:domain :Instrumento .


###  http://rpcw.di.uminho.pt/2024/musica#nome
:nome rdf:type owl:DatatypeProperty ;
        rdfs:domain :Aluno .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/2024/musica#Aluno
:Aluno rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#Curso
:Curso rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/2024/musica#Instrumento
:Instrumento rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

"""


for instrumento in bd["instrumentos"]:
    instrumento["#text"] = instrumento["#text"].replace(" ", "_")
    ttl+=f"""

###  http://rpcw.di.uminho.pt/2024/musica#{instrumento["#text"]}
:{instrumento["#text"]} rdf:type owl:NamedIndividual ;
            :idinstrumento "{instrumento["id"]}" ;
            :instrumento "{instrumento["#text"]}" .

"""

for curso in bd["cursos"]:
    curso["instrumento"]["#text"] = curso["instrumento"]["#text"].replace(" ", "_")
    curso["designacao"] = curso["designacao"].replace(" ", "_")
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/musica#{curso["id"]}
:{curso["id"]} rdf:type owl:NamedIndividual ;
        :ensinaIntrumento :{curso["instrumento"]["#text"]} ;
        :designacao "{curso["designacao"]}" ;
        :duracao {curso["duracao"]} ;
        :idCurso "{curso["id"]}" .

"""

for aluno in bd["alunos"]:
    aluno["nome"]=aluno["nome"].replace(" ", "_")
    aluno["instrumento"] = aluno["instrumento"].replace(" ", "_")
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/musica#{aluno["id"]}
:{aluno["id"]} rdf:type owl:NamedIndividual ;
        :temCurso :{aluno["curso"]} ;
        :temInstrumento :{aluno["instrumento"]} ;
        :anoCurso {aluno["anoCurso"]} ;
        :dataNasc "{aluno["dataNasc"]}" ;
        :idAluno "{aluno["id"]}" ;
        :nome "{aluno["nome"]}" .

"""


# Salve o conteúdo TTL em um arquivo
with open("Musica.ttl", "w", encoding="utf-8") as output_file:
    output_file.write(ttl)

print("Conteúdo guardado.")

