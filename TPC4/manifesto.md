---
Título: TPC4
Data: 12 de Março de 2024
Autor: Afonso Ferreira
UC: RPCW
---

# Tabela Periódica

Este trabalho tem como objetivo a realização de uma página web que utiliza dados provenientes de um repositório GraphDB após a criação e carregamento do arquivo TTL correspondente. A aplicação consiste em páginas interativas relacionadas a elementos químicos e grupos, aproveitando as funcionalidades fornecidas pelo GraphDB.


## Etapas Realizadas

### 1. Criação de um Repositório no GraphDB

Comecei por criar um repositório no GraphDB através de um arquivo TTL com informações de uma tabela periódica.

### 2.  Páginas Web

De seguida entre outros ficheiros foram criadas 5 páginas web:

- **/index** -> Página inicial com a opção de navegar tanto para a página de grupos como dos elementos.

- **/elementos** -> Página com a informação (nome, símbolo, número atómico, número de grupo e nome de grupo) de cada elemento com link de redireção no nome do elemento e no grupo.

- **/grupos** -> Página com a o nome e número de cada grupo

- **/grupo/\<número do grupo\>** | **/grupo/\<nome do grupo\>**  -> Página que apresenta as informações dos elementos de um determinado grupo como o nome, símbolo e número atómico de cada elemento

- **/elemento/\<nome do elemento\>** -> Página que apresenta a informação de um determinado elemento como o nome, símbolo, número atómico, peso atómico, cor, número do grupo, nome do grupo e período.


## Executar a aplicação

É necessário ter um repositório no GraphDB com o nome ```tabelaPeriódica``` e carregar o ficheiro [```tabela_periodica.ttl```](tabela_periodica.ttl). É ainda preciso ter a livraria ```flask``` de Python.

Dentro da pasta ```app_tab_periodica``` basta executar ```python3 app.py```. A página web principal ficará disponível em ```http://127.0.0.1:5000/```.



