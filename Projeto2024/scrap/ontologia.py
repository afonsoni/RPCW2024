import json

def normalize_name(name):
    return name.replace(" ", "_").replace(",", "_").replace("-", "_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")

# Ler o conteúdo do arquivo JSON
with open("dados/regioes_festas.json", encoding="utf-8") as f:
    try:
        festas_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        raise

ttl = """@prefix : <http://rpcw.di.uminho.pt/festas&romarias/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://rpcw.di.uminho.pt/festas&romarias/> .

<http://rpcw.di.uminho.pt/festas&romarias> rdf:type owl:Ontology .

#################################################################
#    Object Properties
#################################################################

###  http://rpcw.di.uminho.pt/festas&romarias#regiaoTemFesta
<http://rpcw.di.uminho.pt/festas&romarias#regiaoTemFesta> rdf:type owl:ObjectProperty ;
                                                          owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#ocorreRegiao> .


###  http://rpcw.di.uminho.pt/festas&romarias#distritoTemFesta
<http://rpcw.di.uminho.pt/festas&romarias#distritoTemFesta> rdf:type owl:ObjectProperty ;
                                                            owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#ocorreDistrito> .


###  http://rpcw.di.uminho.pt/festas&romarias#concelhoTemFesta
<http://rpcw.di.uminho.pt/festas&romarias#concelhoTemFesta> rdf:type owl:ObjectProperty ;
                                                            owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#ocorreConcelho> .


###  http://rpcw.di.uminho.pt/festas&romarias#freguesiaTemFesta
<http://rpcw.di.uminho.pt/festas&romarias#freguesiaTemFesta> rdf:type owl:ObjectProperty ;
                                                             owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#ocorreFreguesia> .


###  http://rpcw.di.uminho.pt/festas&romarias#ocorreRegiao
<http://rpcw.di.uminho.pt/festas&romarias#ocorreRegiao> rdf:type owl:ObjectProperty ;
                                                        rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> ;
                                                        rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Regiao> .


###  http://rpcw.di.uminho.pt/festas&romarias#ocorreDistrito
<http://rpcw.di.uminho.pt/festas&romarias#ocorreDistrito> rdf:type owl:ObjectProperty ;
                                                          rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> ;
                                                          rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Distrito> .


###  http://rpcw.di.uminho.pt/festas&romarias#ocorreConcelho
<http://rpcw.di.uminho.pt/festas&romarias#ocorreConcelho> rdf:type owl:ObjectProperty ;
                                                          rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> ;
                                                          rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Concelho> .


###  http://rpcw.di.uminho.pt/festas&romarias#ocorreFreguesia
<http://rpcw.di.uminho.pt/festas&romarias#ocorreFreguesia> rdf:type owl:ObjectProperty ;
                                                           rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> ;
                                                           rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Freguesia> .


###  http://rpcw.di.uminho.pt/festas&romarias#pertenceRegiao
<http://rpcw.di.uminho.pt/festas&romarias#pertenceRegiao> rdf:type owl:ObjectProperty ;
                                                          owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#temDistrito> .


###  http://rpcw.di.uminho.pt/festas&romarias#pertenceDistrito
<http://rpcw.di.uminho.pt/festas&romarias#pertenceDistrito> rdf:type owl:ObjectProperty ;
                                                            owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#temConcelho> .


###  http://rpcw.di.uminho.pt/festas&romarias#pertenceConcelho
<http://rpcw.di.uminho.pt/festas&romarias#pertenceConcelho> rdf:type owl:ObjectProperty ;
                                                            owl:inverseOf <http://rpcw.di.uminho.pt/festas&romarias#temFreguesia> .


###  http://rpcw.di.uminho.pt/festas&romarias#temDistrito
<http://rpcw.di.uminho.pt/festas&romarias#temDistrito> rdf:type owl:ObjectProperty ;
                                                       rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Regiao> ;
                                                       rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Distrito> .


###  http://rpcw.di.uminho.pt/festas&romarias#temConcelho
<http://rpcw.di.uminho.pt/festas&romarias#temConcelho> rdf:type owl:ObjectProperty ;
                                                       rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Distrito> ;
                                                       rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Concelho> .


###  http://rpcw.di.uminho.pt/festas&romarias#temFreguesia
<http://rpcw.di.uminho.pt/festas&romarias#temFreguesia> rdf:type owl:ObjectProperty ;
                                                        rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Concelho> ;
                                                        rdfs:range <http://rpcw.di.uminho.pt/festas&romarias#Freguesia> .


#################################################################
#    Data properties
#################################################################

###  http://rpcw.di.uminho.pt/festas&romarias#nome
<http://rpcw.di.uminho.pt/festas&romarias#nome> rdf:type owl:DatatypeProperty .


###  http://rpcw.di.uminho.pt/festas&romarias#descricao
<http://rpcw.di.uminho.pt/festas&romarias#descricao> rdf:type owl:DatatypeProperty ;
                                                     rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> .


###  http://rpcw.di.uminho.pt/festas&romarias#dataInicio
<http://rpcw.di.uminho.pt/festas&romarias#dataInicio> rdf:type owl:DatatypeProperty ;
                                                      rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> .


###  http://rpcw.di.uminho.pt/festas&romarias#dataFim
<http://rpcw.di.uminho.pt/festas&romarias#dataFim> rdf:type owl:DatatypeProperty ;
                                                   rdfs:domain <http://rpcw.di.uminho.pt/festas&romarias#Festa> .


#################################################################
#    Classes
#################################################################

###  http://rpcw.di.uminho.pt/festas&romarias#Regiao
<http://rpcw.di.uminho.pt/festas&romarias#Regiao> rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/festas&romarias#Distrito
<http://rpcw.di.uminho.pt/festas&romarias#Distrito> rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/festas&romarias#Concelho
<http://rpcw.di.uminho.pt/festas&romarias#Concelho> rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/festas&romarias#Freguesia
<http://rpcw.di.uminho.pt/festas&romarias#Freguesia> rdf:type owl:Class .


###  http://rpcw.di.uminho.pt/festas&romarias#Festa
<http://rpcw.di.uminho.pt/festas&romarias#Festa> rdf:type owl:Class .


#################################################################
#    Individuals
#################################################################

"""

'''
Exemplo de individuos:
###  http://rpcw.di.uminho.pt/festas&romarias#Aveiro
<http://rpcw.di.uminho.pt/festas&romarias#Aveiro> rdf:type owl:NamedIndividual ,
                                                           <http://rpcw.di.uminho.pt/festas&romarias#Distrito> ;
                                                  <http://rpcw.di.uminho.pt/festas&romarias#nome> "Aveiro" .


###  http://rpcw.di.uminho.pt/festas&romarias#Aveiro1
<http://rpcw.di.uminho.pt/festas&romarias#Aveiro1> rdf:type owl:NamedIndividual ,
                                                            <http://rpcw.di.uminho.pt/festas&romarias#Festa> ;
                                                   <http://rpcw.di.uminho.pt/festas&romarias#ocorreDistrito> <http://rpcw.di.uminho.pt/festas&romarias#Aveiro> ;
                                                   <http://rpcw.di.uminho.pt/festas&romarias#dataFim> "" ;
                                                   <http://rpcw.di.uminho.pt/festas&romarias#dataInicio> "06-01-2024" ;
                                                   <http://rpcw.di.uminho.pt/festas&romarias#descricao> "Com pequeno auto teatral e leilão das ofertas" ;
                                                   <http://rpcw.di.uminho.pt/festas&romarias#nome> "Cortejo dos Reis" .


###  http://rpcw.di.uminho.pt/festas&romarias#BeiraLitoral
<http://rpcw.di.uminho.pt/festas&romarias#BeiraLitoral> rdf:type owl:NamedIndividual ,
                                                                 <http://rpcw.di.uminho.pt/festas&romarias#Regiao> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#regiaoTemFesta> <http://rpcw.di.uminho.pt/festas&romarias#Aveiro1> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#temDistrito> <http://rpcw.di.uminho.pt/festas&romarias#Aveiro> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#nome> "Beira Litoral" .


###  http://rpcw.di.uminho.pt/festas&romarias#SeverDoVouga
<http://rpcw.di.uminho.pt/festas&romarias#SeverDoVouga> rdf:type owl:NamedIndividual ,
                                                                 <http://rpcw.di.uminho.pt/festas&romarias#Concelho> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#concelhoTemFesta> <http://rpcw.di.uminho.pt/festas&romarias#Aveiro1> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#pertenceDistrito> <http://rpcw.di.uminho.pt/festas&romarias#Aveiro> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#temFreguesia> <http://rpcw.di.uminho.pt/festas&romarias#Talhadas> ;
                                                        <http://rpcw.di.uminho.pt/festas&romarias#nome> "Sever do Vouga" .


###  http://rpcw.di.uminho.pt/festas&romarias#Talhadas
<http://rpcw.di.uminho.pt/festas&romarias#Talhadas> rdf:type owl:NamedIndividual ,
                                                             <http://rpcw.di.uminho.pt/festas&romarias#Freguesia> ;
                                                    <http://rpcw.di.uminho.pt/festas&romarias#freguesiaTemFesta> <http://rpcw.di.uminho.pt/festas&romarias#Aveiro1> ;
                                                    <http://rpcw.di.uminho.pt/festas&romarias#nome> "Talhadas" .
'''

# Adicionar festas
for festa in festas_data["festas"]:
    ttl += f"""
###  http://rpcw.di.uminho.pt/festas&romarias#{festa["festa_id"]}
:{festa["festa_id"]} rdf:type owl:NamedIndividual ,
        :Festa ;
        :nome "{festa["nome"]}" ;
        :descricao "{festa["descricao"]}" ;
        :dataInicio "{festa["data_inicio"]}" ;
        :dataFim "{festa["data_fim"]}" ;
        :ocorreRegiao :{festa["regiao"]} ;
        :ocorreDistrito :{normalize_name(festa["distrito"])} ;
        :ocorreConcelho :{normalize_name(festa["concelho"])} """
    if festa["freguesia"]:
            ttl += f""" ;
        :ocorreFreguesia :{normalize_name(festa["freguesia"])} .
        
        
        """
    else:
            ttl += " .\n\n"        


# Adicionar regiões
for regiao in festas_data["regioes"]:
    ttl += f"""
###  http://rpcw.di.uminho.pt/festas&romarias#{normalize_name(regiao["regiao"])}
:{normalize_name(regiao["regiao"])} rdf:type owl:NamedIndividual ,
        :Regiao ;
        :nome "{regiao["regiao"]}" ;
"""
    for festa in festas_data["festas"]:
        if festa["regiao"] == regiao:
            ttl += f"""
        :regiaoTemFesta :{festa["festa_id"]} ;
"""
    for distrito in regiao["distritos"]:
        ttl += f"""        :temDistrito :{normalize_name(distrito["distrito"])} ;
"""
        # Último distrito não deve ter ponto e vírgula
        if distrito == regiao["distritos"][-1]:
            ttl = ttl[:-2] + " .\n"

    for distrito in regiao["distritos"]:
        ttl += f"""
### http://rpcw.di.uminho.pt/festas&romarias#{normalize_name(distrito["distrito"])}
:{normalize_name(distrito["distrito"])} rdf:type owl:NamedIndividual ,
        :Distrito ;
        :nome "{distrito["distrito"]}" ;
        :pertenceRegiao :{normalize_name(regiao["regiao"])} ;
"""
        for festa in festas_data["festas"]:
            if festa["distrito"] == distrito:
                ttl += f"""
        :distritoTemFesta :{festa["festa_id"]} ;"""

        for concelho in distrito["concelhos"]:
            ttl += f"""
        :temConcelho :{normalize_name(concelho["concelho"])} ;
"""
            # Último concelho não deve ter ponto e vírgula
            if concelho == distrito["concelhos"][-1]:
                ttl = ttl[:-2] + " .\n"

        for concelho in distrito["concelhos"]:
            ttl += f"""
### http://rpcw.di.uminho.pt/festas&romarias#{normalize_name(concelho["concelho"])}
:{normalize_name(concelho["concelho"])} rdf:type owl:NamedIndividual ,
        :Concelho ;
        :nome "{concelho["concelho"]}" ;
        :pertenceDistrito :{normalize_name(distrito["distrito"])} ;
"""
            for festa in festas_data["festas"]:
                if festa["concelho"] == concelho:
                    ttl += f"""
        :concelhoTemFesta :{festa["festa_id"]} ;
"""

            for freguesia in concelho["freguesias"]:
                ttl += f"""        :temFreguesia :{normalize_name(freguesia)} ;
"""

                # Última freguesia não deve ter ponto e vírgula
                if freguesia == concelho["freguesias"][-1]:
                    ttl = ttl[:-2] + " .\n"

            for freguesia in concelho["freguesias"]:
                ttl += f"""
### http://rpcw.di.uminho.pt/festas&romarias#{normalize_name(freguesia)}
:{normalize_name(freguesia)} rdf:type owl:NamedIndividual ,
        :Freguesia ;
        :nome "{freguesia}" ;
        :pertenceConcelho :{normalize_name(concelho["concelho"])} """

                for festa in festas_data["festas"]:
                    if festa["freguesia"] == freguesia:
                        ttl += f""";
        :freguesiaTemFesta :{festa["festa_id"]}"""
                    if festa == festas_data["festas"][-1]:
                        ttl += " .\n"

# Salvar o conteúdo TTL em um novo arquivo
with open("dados/festas_povoadas.ttl", "w", encoding="utf-8") as output_file:
    output_file.write(ttl)

print("Conteúdo guardado em festas_povoadas.ttl.")

