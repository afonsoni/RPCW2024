---
Título: TPC2
Data: 25 de fevereiro de 2024
Autor: Afonso Ferreira
UC: RPCW
---

# Dataset Escola de Música

Este trabalho tem como objetivo analisar, modelar e representar um conjunto de dados relacionados a uma Escola de Música. O dataset inclui informações sobre alunos, instrumentos e cursos.

## Etapas Realizadas

### 1. Análise do Dataset

Foi realizada uma análise detalhada do dataset, identificando informações redundantes e inconsistências. Assegurando que os dados estavam prontos para serem utilizados na modelagem da ontologia.

### 2. Criação da Ontologia

Foi desenvolvida uma ontologia para representar de forma estruturada e semântica as entidades presentes no dataset:

- **Classes:** Aluno, Instrumento e Curso.
- **Object Properties:** ensinaInstrumento, temCurso, temInstrumento.
- **Data Properties:** anoCurso, dataNasc, designacao, duracao, idAluno, idCurso, idInstrumento, instrumento, nome.

### 3. Script de Povoamento da Ontologia

De seguida, foi elaborada um script para popular a ontologia com os dados do dataset. Esse script assegura que todas as instâncias e relações sejam corretamente representadas na ontologia.

### 4. Criação de um Repositório no GraphDB

Por fim, foi implementado um repositório no GraphDB para armazenar e visualizar a ontologia.
