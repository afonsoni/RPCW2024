import json

'''
Vou adicionar uma festa_id para cada festa, para que seja mais fácil identificar cada uma delas.

{
    "regioes": [
        {
            "regiao": "beira_litoral",
            "distritos": [
                {
                    "distrito": "Aveiro",
                    "concelhos": [
                        {
                            "concelho": "Águeda",
                            "freguesias": [
                                "Aguada de Cima",
                                "Fermentelos",
                                "Macinhata do Vouga",
                                "Valongo do Vouga",
                                "União das freguesias de Águeda e Borralha",
                                "União das freguesias de Barrô e Aguada de Baixo",
                                "União das freguesias de Belazaima do Chão, Castanheira do Vouga e Agadão",
                                "União das freguesias de Recardães e Espinhel",
                                "União das freguesias de Travassô e Óis da Ribeira",
                                "União das freguesias de Trofa, Segadães e Lamas do Vouga",
                                "União das freguesias do Préstimo e Macieira de Alcoba"
                            ]
                        },
                        {
                            "concelho": "Albergaria-a-Velha",
                            "freguesias": [
                                "Alquerubim",
                                "Angeja",
                                "Branca",
                                "Ribeira de Fráguas",
                                "Albergaria-a-Velha e Valmaior",
                                "São João de Loure e Frossos"
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    "festas": [
        {
            "festa_id": 1,
            "Nome": "Cortejo dos Reis",
            "Descrição": "com pequeno auto teatral e leilão das ofertas",
            "Data Início": "06-01-2024",
            "Data Fim": "06-01-2024",
            "Região": "beira_litoral",
            "Distrito": "Aveiro",
            "Concelho": "Sever do Vouga",
            "Freguesia": "Talhadas"
        },
        {
            "Nome": "Romaria dos Santos Mártires",
            "Descrição": "Procissão dos Nus, antigamente composta por fiéis amortalhados em cumprimento das suas promessas: No dia seguinte, nova procissão, em que as crianças passam por debaixo do andor de Santa Clara, para não se atrasarem no falar.",
            "Data Início": "07-01-2024",
            "Data Fim": "07-01-2024",
            "Região": "beira_litoral",
            "Distrito": "Aveiro",
            "Concelho": "Águeda",
            "Freguesia": "Travassô"
        },
        {
            "Nome": "Festa das Fogaceiras",
            "Descrição": "importantíssima romaria celebrando S. Sebastião. Na procissão, meninas de branco levam as fogaças à cabeça.",
            "Data Início": "20-01-2024",
            "Data Fim": "20-01-2024",
            "Região": "beira_litoral",
            "Distrito": "Aveiro",
            "Concelho": "Santa Maria da Feira",
            "Freguesia": "Santa Maria da Feira"
        }
    ]
}
'''

# Caminho para o JSON
file_path = 'festas_combinadas.json'

# Carregar o ficheiro JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
# Adicionar um ID a cada festa
for i, festa in enumerate(data['festas'], start=1):
    festa['festa_id'] = i
    
# Guardar o resultado num ficheiro JSON
with open('festas_combinadas_com_id.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
    
print('Ficheiro JSON criado com sucesso!')