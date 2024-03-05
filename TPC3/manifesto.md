---
Título: TPC3
Data: 3 de Março de 2024
Autor: Afonso Ferreira
UC: RPCW
---

# Dataset Mapa Virtual

Este trabalho tem como objetivo analisar, modelar e representar um conjunto de dados relacionados a um mapa virtual. O dataset inclui informações sobre cidades e as suas ligações.

## Etapas Realizadas

### 1. Análise do Dataset

Foi realizada uma análise detalhada do dataset, identificando informações redundantes e inconsistências. Assegurando que os dados estavam prontos para serem utilizados na modelagem da ontologia.

### 2. Criação da Ontologia

Foi desenvolvida uma ontologia para representar de forma estruturada e semântica as entidades presentes no dataset:

- **Classes:** Cidade, Ligação.
- **Object Properties:** ensinaInstrumento, temCurso, temInstrumento.
- **Data Properties:** 
    - ***cidade*** - id, nome, população, descrição, distrito.
    - ***ligação*** - id, distância.

### 3. Script de Povoamento da Ontologia

De seguida, foi elaborada um script para popular a ontologia com os dados do dataset. Esse script assegura que todas as instâncias e relações sejam corretamente representadas na ontologia.

### 4. Criação de um Repositório no GraphDB

Posteriormente foi implementado um repositório no GraphDB para armazenar e visualizar a ontologia.

### 5 . Especcificamento de Queries

Por mim, foram criadas 4 queries atrvés do SPARQL de modo a responder as seguintes perguntas:

1. Quais as cidades de um determinado distrito?

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

select ?nome where { 
	?s :distrito "Braga" ;
    	:nome ?nome .
}
```


2. Distribuição de cidades por distrito?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

select ?distrito (Count(?cidade) as ?nCidade) where {
    ?cidade :distrito ?distrito .
}
GROUP By ?distrito
ORDER BY ?distrito
```

3. Quantas cidades se podem atingir a partir do Porto? (Diretamente)
```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

select distinct ?cidade where {
    ?nome :distrito "Porto" .
    ?ligacao :origem ?porto .
    ?ligacao :destino ?c .
    ?c :nome ?cidade .   
}
```


4. Quais as cidades com população acima de um determinado valor?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa/>

select ?cidade ?populacao where {
	?c :nome ?cidade ;
       :populacao ?populacao .
    FILTER(?populacao > 250000)
}
ORDER BY ?cidade
```