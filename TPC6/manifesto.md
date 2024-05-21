---
Título: TPC6
Data: 1 de Abril de 2024
Autor: Afonso Ferreira
UC: RPCW
---

Este trabalho tinha como objetivo final a geração de uma interface web com informação de filmes. Para isso foi dividido em 3 fases:

### JSON to Turtle

Para a primeira fase, foi feita a transformação de um ficheiro json numa ontologia em `.ttl`e foi carregado esse último ficheiro para o endpoint disponibilizado pelo professor (`http://epl.di.uminho.pt:7200`) 

---

### SPARQL queries

Numa segunda fase foram feitas as seguintes queries:

1. Quantos filmes existem no repositório?

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select (COUNT(?s) as ?nfilmes) where {
    ?s a :Film .
}
```


2. Qual a distribuição de filmes por ano de lançamento?



```sql
...
```

3. Qual a distribuição de filmes por género?



```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?genre (COUNT(?s) as ?nfilmes) where {
    ?s a :Film .
    ?s :hasGenre ?genre.
} 
GROUP BY (?genre)
ORDER BY DESC (?nfilmes)
```

4. Em que filmes participou o ator "Burt Reynolds"?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?s where {
    ?s a :Film .
    ?s :hasActor :Burt_Reynolds.
} 
```

5. Produz uma lista de realizadores com o seu nome e o número de filmes que realizou.


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?director (COUNT(?s) as ?nfilmes) where {
    ?s a :Film .
    ?s :hasDirector ?director.
} 
GROUP BY (?director)
ORDER BY DESC (?nfilmes)
```

6. Qual o título dos livros que aparecem associados aos filmes?


```sql
...
```

---

### Aplicação Web

Quanto à aplicação web, optou-se por ter 7 páginas diferentes:
-   `/` - Página inicial onde se pode escolher entre filmes, realizadores e atores.
-   `/filmes` - mostra uma tabela com todos os filmes (o seu titulo e a sua duração). O título tem uma referência para a página do respetivo filme.
-  `/filmes/:titulo` - mostra a página do filme com a respetiva informação: título, descrição, duração, géneros, países, realizadores, atores,compositores, produtores e argumentistas
-  `/realizadores` - mostra uma tabela com todos os realizadores (o seu nome e o número de filmes que realizaram ordenados por ordem descrescente de filmes realizados). 
-  `/realizadores/:nome` - mostra a lista dos filmes que realizaram
-  `/atores` - mostra uma tabela com todos os atores (o seu nome e o número de filmes em que atuaram ordenados por ordem descrescente).
-  `/atores/:nome` - mostra a lista dos filmes em que atuaram

---

