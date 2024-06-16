import pandas as pd
import json

# Carregar o ficheiro Excel
file_path = 'dados/FreguesiasPortugalMetadata.xlsx'
df = pd.read_excel(file_path)

# Estrutura para armazenar os dados
data = {}

# Preencher a estrutura
for _, row in df.iterrows():
    regiao = row['provincia']
    distrito = row['distrito']
    concelho = row['concelho']
    freguesia = row['freguesia']
    
    if regiao not in data:
        data[regiao] = {}
    if distrito not in data[regiao]:
        data[regiao][distrito] = {}
    if concelho not in data[regiao][distrito]:
        data[regiao][distrito][concelho] = []
    if freguesia not in data[regiao][distrito][concelho]:
        data[regiao][distrito][concelho].append(freguesia)

# Converter para o formato desejado
output = []
for regiao, distritos in data.items():
    regiao_obj = {"regiao": regiao, "distritos": []}
    for distrito, concelhos in distritos.items():
        distrito_obj = {"distrito": distrito, "concelhos": []}
        for concelho, freguesias in concelhos.items():
            concelho_obj = {"concelho": concelho, "freguesias": freguesias}
            distrito_obj["concelhos"].append(concelho_obj)
        regiao_obj["distritos"].append(distrito_obj)
    output.append(regiao_obj)

# Converter para JSON
json_output = json.dumps(output, ensure_ascii=False, indent=4)

# Salvar em um ficheiro JSON
with open('dados/regioes.json', 'w', encoding='utf-8') as f:
    f.write(json_output)

print(json_output)