import os
import re
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from fuzzywuzzy import process, fuzz
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta, SU, MO, TU, WE, TH, FR, SA


# Configurar o User-Agent
ua = UserAgent()
headers = {'User-Agent': ua.random}

df = pd.read_excel('dados/FreguesiasPortugalMetadata.xlsx')

# Inicializa o contador de IDs
global festa_id_counter
festa_id_counter = 0

'''
Casos de linhas:
freg , conc , data - nome : desc
freg , conc , data - nome . desc (ponto não pode ser antecedido por letra maiúscula)
freg , conc , data : nome . desc
freg , conc , data - nome , +desc
freg , conc , data : nome , +desc
freg , conc , data - nome
conc , data : nome . desc
conc , data : nome , +desc
freg , conc - data+nome : desc
conc , data - nome , +desc
conc , data - nome . desc
conc , data - nome
freg , conc , data+nome . desc

Ver se frase contém travessão ou dois pontos
Dividir a frase pelo primeiro travessão específico - ou dois pontos :
Feita a divisão, pegando na primeira parte:
Divide-se a primeira parte por vírgulas
- Se houver 2 elementos, o primeiro é o concelho e o segundo é a data
    - Há um outlier: freguesia, concelho. Tem de se ver sempre se o segundo elemento é um concelho através do mapeamento. Se for, é o concelho, senão é a data
- Se houver 3 elementos, o primeiro é a freguesia, o segundo é o concelho e o terceiro é a data
Para filtrar a freguesia e o concelho, é necessário ir ao mapeamento e filtrar pela região onde se inserem na web
Dividir a segunda parte pela primeira ocasião de dois pontos, vírgula ou ponto final. Apenas se divide a primeira vez.
O primeiro será o nome e o segundo será a descrição
No caso de haver uma vírgula, o nome é o primeiro elemento e a descrição é a junção dos dois.
Nos restantes casos, o nome é o primeiro elemento e a descrição é o segundo
'''

# Função para armazenar os dados das regiões, distritos, concelhos e freguesias num ficheiro JSON
def store_regioes():
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

    # Salvar num ficheiro JSON
    with open('dados/regioes.json', 'w', encoding='utf-8') as f:
        f.write(json_output)

def incrementar_id():
    global festa_id_counter
    festa_id_counter += 1
    return festa_id_counter

def concelho_exists_in_regiao(concelho, regiao, threshold=80):
    print("Concelho_exists_in_regiao", concelho, regiao)
    # Substituir "da" e "de" por um padrão opcional na expressão regular
    concelho_escaped = re.escape(concelho)
    concelho_pattern = re.sub(r'\b(de|da|do)\b', r'(de|da|do)?', concelho_escaped, flags=re.IGNORECASE)
    # filtrar pela região e concelho. O concelho não precisa de estar acentuado, nem em maiúsculas, nem tem de estar completo
    filtered_df = df[(df['provincia'].str.contains(regiao)) & (df['concelho'].str.contains(concelho_pattern, case=False, regex=True, na=False))]
    if filtered_df.empty:
        filtered_df = df[(df['provincia'].str.contains(regiao))]
        # Usar fuzzywuzzy para encontrar o concelho mais próximo
        matches = process.extract(concelho, filtered_df['concelho'], scorer=fuzz.token_set_ratio)
        best_match = matches[0] if matches and matches[0][1] >= threshold else None
        if best_match:
            concelho = best_match[0].strip()
            distrito = filtered_df[filtered_df['concelho'] == concelho]['distrito'].iloc[0].strip()
            return concelho, distrito
        else:
            return None, None
    else:
    # ir buscar o primeiro concelho e distrito
        concelho = filtered_df['concelho'].iloc[0].strip()
        distrito = filtered_df['distrito'].iloc[0].strip()
        return concelho, distrito

def freguesia_exists_in_regiao(freguesia, concelho, regiao, threshold=80):
    print("Freguesia_exists_in_regiao", freguesia, concelho, regiao)
    # Substituir "da" e "de" por um padrão opcional na expressão regular
    freguesia_escaped = re.escape(freguesia)
    freguesia_pattern = re.sub(r'\b(de|da|do)\b', r'(de|da|do)?', freguesia_escaped, flags=re.IGNORECASE)
    # filtrar pela região e freguesia. A freguesia não precisa de estar acentuado, nem em maiúsculas, nem tem de estar completo
    if concelho:
        concelho_escaped = re.escape(concelho)
        filtered_df = df[(df['provincia'].str.contains(regiao)) & 
                        (df['concelho'].str.contains(concelho_escaped, case=False, regex=True, na=False)) & 
                        (df['freguesia'].str.contains(freguesia_pattern, case=False, regex=True, na=False))]
    else:
        filtered_df = df[(df['provincia'].str.contains(regiao)) & 
                        (df['freguesia'].str.contains(freguesia_pattern, case=False, regex=True, na=False))]
    if filtered_df.empty:
        if concelho:
            filtered_df = df[(df['provincia'].str.contains(regiao)) & (df['concelho'].str.contains(concelho_escaped, case=False, regex=True, na=False))]
        else:
            filtered_df = df[(df['provincia'].str.contains(regiao))]
        # Usar fuzzywuzzy para encontrar a freguesia mais próxima
        matches = process.extract(freguesia, filtered_df['freguesia'], scorer=fuzz.token_set_ratio)
        best_match = matches[0] if matches and matches[0][1] >= threshold else None
        if best_match:
            freguesia = best_match[0].strip()
            concelho = filtered_df[filtered_df['freguesia'] == freguesia]['concelho'].iloc[0].strip()
            distrito = filtered_df[filtered_df['freguesia'] == freguesia]['distrito'].iloc[0].strip()
            return freguesia, concelho, distrito
        else:
            return None, None, None
    else:
    # ir buscar o primeiro concelho e distrito
        freguesia = filtered_df['freguesia'].iloc[0].strip()
        concelho = filtered_df['concelho'].iloc[0].strip()
        distrito = filtered_df['distrito'].iloc[0].strip()
        return freguesia, concelho, distrito
    


def two_elements(part, regiao):
    # Em princípio o primeiro elemento é concelho, o segundo é a data.
    # Tem de se ver primeiro se o segundo elemento é um concelho através do mapeamento.
    locais = concelho_exists_in_regiao(part[1].strip(),regiao)

    # Se o segundo elemento estiver nos concelhos, é porque o segundo elemento é um concelho e o primeiro é freguesia, senão é data
    if locais != (None, None):
        freguesia, concelho, distrito = freguesia_exists_in_regiao(part[0].strip(),part[1].strip(),regiao)
        print("locais != 0", freguesia, concelho, distrito)
        data = None
    else:
        freguesia = None
        concelho, distrito = concelho_exists_in_regiao(part[0].strip(),regiao)
        if concelho == None:
            freguesia, concelho, distrito = freguesia_exists_in_regiao(part[0].strip(),None,regiao)
        data = part[1].strip()
    return freguesia, concelho, distrito, data

def three_elements(part, regiao):
    freguesia, concelho, distrito = freguesia_exists_in_regiao(part[0].strip(),part[1].strip(),regiao)
    if freguesia == None:
        freguesia = part[0].strip()
        concelho, distrito = concelho_exists_in_regiao(part[1].strip(),regiao)
    data = part[2].strip()
    return freguesia, concelho, distrito, data

def get_nome_descricao(part):
    # Use a lookahead assertion to capture all characters until the first match of the separator pattern
    match = re.search(r'^(.*?)(?=([^A-Z]\.|,|:))', part)
    if match:
        # se existir um ponto no group(2), é porque se tem de juntar os dois grupos
        if '.' in match.group(2):
            nome = match.group(1).strip() + match.group(2).strip()
        else:
            nome = match.group(1).strip()
        # Find the separator after the captured part
        separator_match = re.search(r'[^A-Z]\.|,|:', part[match.end():])
        if separator_match:
            separator = separator_match.group()
            descricao = part[match.end():].split(separator, 1)[1].strip()
        else:
            descricao = part[match.end():].strip()
    else:
        nome = part.strip()
        descricao = None
    
    if nome[-1] == '.':
        nome = nome[:-1].strip()
    descricao = descricao[0].upper() + descricao[1:] if descricao else None

    return nome, descricao
# Função para calcular a data da Páscoa
def calcular_pascoa(ano):
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mes = (h + l - 7 * m + 114) // 31
    dia = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(ano, mes, dia)

# Função para calcular eventos móveis
def calcular_eventos_moveis(ano):
    pascoa = calcular_pascoa(ano)
    domingo_ramos = pascoa - timedelta(days=7)
    sexta_santa = pascoa - timedelta(days=2)
    sabado_aleluia = pascoa - timedelta(days=1)
    segunda_pascoa = pascoa + timedelta(days=1)
    domingo_pascoela = pascoa + timedelta(days=7)
    segundo_domingo_pascoa = pascoa + timedelta(days=14)
    quinta_ascensao = pascoa + timedelta(days=39)
    domingo_espirito_santo = pascoa + timedelta(days=49)
    domingo_lazaro = pascoa - timedelta(days=14)
    penultima_sexta_quaresma = pascoa - timedelta(days=15)
    quinto_domingo_pascoa = pascoa + timedelta(days=35)
    terceiro_domingo_pascoa = pascoa + timedelta(days=21)
    segundo_domingo_quaresma = pascoa - timedelta(days=35)
    terca_feira_gorda = pascoa - timedelta(days=47)
    quinta_feira_santa = pascoa - timedelta(days=3)
    dia_corpo_deus = pascoa + timedelta(days=60)
    quarto_domingo_quaresma = pascoa - timedelta(days=21)
    domingo_santissima_trindade = pascoa + timedelta(days=56)
    quinta_feira_santa_40_dias = pascoa + timedelta(days=39)
    segunda_pascoela = pascoa + timedelta(days=8)
    terca_pascoela = pascoa + timedelta(days=9)
    domingo_pascoela_impares = pascoa + timedelta(days=7) if ano % 2 != 0 else None
    num_domingos_quaresma = pascoa - timedelta(days=49) + relativedelta(weekday=SU(+1))
    quinta_antes_domingo_gordo = pascoa - timedelta(days=52)

    return {
        "Domingo de Ramos": domingo_ramos,
        "Sexta-feira Santa": sexta_santa,
        "Sábado de Aleluia": sabado_aleluia,
        "Domingo de Páscoa": pascoa,
        "Segunda-feira de Páscoa": segunda_pascoa,
        "Domingo de Pascoela": domingo_pascoela,
        "2º domingo depois da Páscoa": segundo_domingo_pascoa,
        "5ª feira da Ascensão": quinta_ascensao,
        "Domingo do Espírito Santo": domingo_espirito_santo,
        "Domingo de Lázaro": domingo_lazaro,
        "penúltima sexta-feira da Quaresma": penultima_sexta_quaresma,
        "quinto domingo depois de Páscoa": quinto_domingo_pascoa,
        "domingo terceiro de Páscoa": terceiro_domingo_pascoa,
        "2º domingo da Quaresma": segundo_domingo_quaresma,
        "terça-feira gorda": terca_feira_gorda,
        "quinta-feira santa": quinta_feira_santa,
        "dia de corpo de deus": dia_corpo_deus,
        "4º domingo da quaresma": quarto_domingo_quaresma,
        "domingo da santíssima trindade": domingo_santissima_trindade,
        "5ª feira da ascensão (40 dias após a páscoa)": quinta_feira_santa_40_dias,
        "segunda-feira de pascoela": segunda_pascoela,
        "terça-feira de pascoela": terca_pascoela,
        "domingo de pascoela (nos anos ímpares)": domingo_pascoela_impares,
        "num dos domingos da quaresma": num_domingos_quaresma,
        "quinta-feira anterior a domingo gordo": quinta_antes_domingo_gordo
    }

# Função para converter expressões como 'primeiro domingo de outubro' para uma data normal
def convert_to_date(text, year):
    eventos_moveis = calcular_eventos_moveis(year)
    text_lower = text.lower()
    for evento, data in eventos_moveis.items():
        if data and evento.lower() in text_lower:
            return data.strftime('%d/%m/%Y')

    month_mapping = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
        'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
        'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    
    weekday_mapping = {
        'domingo': SU, 'segunda': MO, 'terça': TU, 'quarta': WE, 'quinta': TH, 'sexta': FR, 'sábado': SA
    }

    for month_name, month_number in month_mapping.items():
        if month_name in text_lower:
            break
    else:
        return text  # Retorna o texto original se não encontrar o mês
    
    if 'semana' in text_lower:
        if 'primeira' in text_lower:
            nth = 1
        elif 'segunda' in text_lower:
            nth = 2
        elif 'terceira' in text_lower:
            nth = 3
        elif 'quarta' in text_lower:
            nth = 4
        else:
            return text  # Retorna o texto original se não encontrar a ocorrência
        first_day_of_month = datetime(year, month_number, 1)
        target_date = first_day_of_month + relativedelta(weeks=nth-1, weekday=MO(0))
        return target_date.strftime('%d/%m/%Y')
    
    for weekday_name, weekday in weekday_mapping.items():
        if weekday_name in text_lower:
            break
    else:
        return text  # Retorna o texto original se não encontrar o dia da semana

    nth = re.search(r'\b(primeiro|segundo|terceiro|quarto|quinto|último)\b', text_lower)
    if nth:
        nth = {
            'primeiro': 1, 'segundo': 2, 'terceiro': 3, 'quarto': 4, 'quinto': 5, 'último': -1
        }[nth.group(0)]
    else:
        return text  # Retorna o texto original se não encontrar a ocorrência

    first_day_of_month = datetime(year, month_number, 1)
    if nth == -1:
        next_month = first_day_of_month + relativedelta(months=1)
        last_day_of_month = next_month - relativedelta(days=1)
        target_date = last_day_of_month + relativedelta(weekday=weekday(-1))
    else:
        target_date = first_day_of_month + relativedelta(weekday=weekday(nth))
    
    return target_date.strftime('%d/%m/%Y')

def parse_data(data):
    if any(keyword in data.lower() for keyword in ['primeiro', 'segundo', 'terceiro', 'quarto', 'quinto', 'último', 'semana']):
        return convert_to_date(data, datetime.now().year)
    
    month_mapping = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
        'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
        'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    for month_name, month_number in month_mapping.items():
        if month_name in data.lower():
            data = data.lower().replace(month_name, str(month_number))
            break
    else:
        return data  # Retorna o texto original se não encontrar o mês
    
    try:
        parsed_date = parse(data, dayfirst=True, fuzzy=True).strftime('%d/%m/%Y')
        return parsed_date
    except ValueError:
        day = re.search(r'\d+', data)
        day = day.group(0) if day else '1'
        
        try:
            date = datetime.strptime(f"{day}/{month_number}/{datetime.now().year}", "%d/%m/%Y")
            formatted_date = date.strftime('%d/%m/%Y')
            return formatted_date
        except ValueError:
            return "sem data"  # Retorna "sem data" se houver erro na formatação da data

def parse_festa(festa, trimester, regiao):
    # Dividir a frase pelo primeiro travessão específico – ou dois pontos :
    if '–' in festa:
        # Dividir a frase apenas pelo primeiro travessão
        parts = festa.split('–', 1)
    elif ':' in festa:
        # Dividir a frase apenas pelos primeiros dois pontos
        parts = festa.split(':', 1)
    else:
        return None

    # Dividir a primeira parte por vírgulas
    first_part = parts[0].strip()
    first_part = first_part.split(',')
    if len(first_part) == 2:
        freguesia, concelho, distrito, data = two_elements(first_part, regiao)
    elif len(first_part) == 3:
        freguesia, concelho, distrito, data = three_elements(first_part, regiao)
    else:
        return None

    # Dividir a segunda parte pela primeira ocasião de dois pontos, vírgula ou ponto final
    second_part = parts[1].strip()
    # Regex que verifica qual é o primeiro dos três elementos a aparecer, ":" ou "," ou "."
    # Se for um ponto, não pode ser antecedido por letra maiúscula
    nome, descricao = get_nome_descricao(second_part)
    if data is None:
        data = nome.strip()

    data = parse_data(data)
    
    eventos_moveis = {
        "domingo de ramos": "Domingo de Ramos",
        "sexta-feira santa": "Sexta-feira Santa",
        "sábado de aleluia": "Sábado de Aleluia",
        "domingo de páscoa": "Domingo de Páscoa",
        "segunda-feira de páscoa": "Segunda-feira de Páscoa",
        "domingo de pascoela": "Domingo de Pascoela",
        "2º domingo depois da páscoa": "2º domingo depois da Páscoa",
        "5ª feira da ascensão": "5ª feira da Ascensão",
        "domingo do espírito santo": "Domingo do Espírito Santo",
        "domingo de lázaro": "Domingo de Lázaro",
        "penúltima sexta-feira da quaresma": "penúltima sexta-feira da Quaresma",
        "quinto domingo depois de páscoa": "quinto domingo depois de Páscoa",
        "domingo terceiro de páscoa": "domingo terceiro de Páscoa",
        "2º domingo da quaresma": "2º domingo da Quaresma",
        "terça-feira gorda": "terça-feira gorda",
        "quinta-feira santa": "quinta-feira santa",
        "dia de corpo de deus": "dia de corpo de deus",
        "4º domingo da quaresma": "4º domingo da quaresma",
        "domingo da santíssima trindade": "domingo da santíssima trindade",
        "5ª feira da ascensão (40 dias após a páscoa)": "5ª feira da ascensão (40 dias após a páscoa)",
        "segunda-feira de pascoela": "segunda-feira de pascoela",
        "terça-feira de pascoela": "terça-feira de pascoela",
        "domingo de pascoela (nos anos ímpares)": "domingo de pascoela (nos anos ímpares)",
        "num dos domingos da quaresma": "num dos domingos da quaresma",
        "quinta-feira anterior a domingo gordo": "quinta-feira anterior a domingo gordo",
    }
    
    if data.lower() in eventos_moveis:
        data = convert_to_date(eventos_moveis[data.lower()], datetime.now().year)
    
    if "carnaval" in data.lower():
        data = "13/02/2024"

    return {
        "nome": nome,
        "descricao": descricao,
        "data_inicio": data,
        "data_fim": None,
        "regiao": regiao,
        "distrito": distrito,
        "concelho": concelho,
        "freguesia": freguesia
    }

# Função para extrair os dados de cada trimestre
def extract_festas_by_trimester(soup, trimester, regiao):
    festas = []
    datas = []
    others = []
    sem_distritos = []
    header = soup.find(string=re.compile(re.sub(r'\s+', r'\\s+', trimester), re.IGNORECASE))
    if header:
        print(f"Região: {regiao}")
        next_elements = header.find_all_next(['p', 'ul'])
        for element in next_elements:
            if element.name == 'p' and trimester not in element.text:
                break
            if element.name == 'ul':
                items = element.find_all('li')
                for item in items:
                    festa = (parse_festa(item.get_text(strip=True), trimester, regiao))
                    if (festa) != None:
                        # Ver se a data início é do estilo '%d/%m/%Y' se não for enviar para outro ficheiro
                        if (festa['data_inicio'] != None):
                            try:
                                datetime.strptime(festa['data_inicio'], '%d/%m/%Y')
                                if (festa['distrito'] != None):
                                    festas.append(festa)
                                    festa_id = incrementar_id()
                                    festa['festa_id'] = festa_id
                                else:
                                    sem_distritos.append(item.get_text(strip=True))
                                    with open('sem_distritos.txt', 'a') as sem_distritos_file:
                                        sem_distritos_file.write(f"Região: {regiao}\n")
                                        sem_distritos_file.write(f"{item.get_text(strip=True)}\n")
                            except ValueError:
                                datas.append(festa)
                    else:
                        others.append(item.get_text(strip=True))
                        with open('outros.txt', 'a') as outros_files:
                            outros_files.write(f"Região: {regiao}\n")
                            outros_files.write(f"{item.get_text(strip=True)}\n")
                
    else:
        print(f"Não encontrado: {trimester}")
    return festas, datas

def process_url(url, regiao):
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        print(f"Acesso negado: 403 Forbidden para {url}")
        return []

    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    trimesters = ['1º trimestre', '2º trimestre', '3º trimestre', '4º trimestre']
    festas_data = {}
    datas_data = {}
    for trimester in trimesters:
        festas, datas = extract_festas_by_trimester(soup, trimester, regiao)
        festas_data[trimester] = festas
        datas_data[trimester] = datas

    rows = []
    for _, festas in festas_data.items():
        if not festas:
            continue
        for festa in festas:
            if festa is not None:
                rows.append(festa)
    rows2 = []
    for _, datas in datas_data.items():
        if not datas:
            continue
        for data in datas:
            if data is not None:
                rows2.append(data)

    return rows, rows2

store_regioes()

# URLs são os links para as páginas de cada região
urls_file = 'urls.txt'
with open(urls_file, 'r') as file:
    lines = file.readlines()

output_dir = 'dados'
os.makedirs(output_dir, exist_ok=True)

all_festas = []
all_datas = []
for line in lines:
    # Cada linha do ficheiro tem a URL e a região
    url, regiao = line.strip().split()
    # Extrair os dados da página
    festas, datas = process_url(url, regiao)
    # Salvar todas as festas num único CSV
    for festa in festas:
        all_festas.append(festa)
    for data in datas:
        all_datas.append(data)
# Salvar todas as festas num único arquivo JSON
with open('festas.json', 'w', encoding='utf-8') as festas_file:
    json.dump(all_festas, festas_file, ensure_ascii=False, indent=4)
with open('datas.json', 'w', encoding='utf-8') as datas_file:
    json.dump(all_datas, datas_file, ensure_ascii=False, indent=4)

# Salvar as festas num CSV
columns = ["festa_id", "nome", "data_inicio", "data_fim", "freguesia", "concelho", "distrito", "descricao", "regiao"]
df = pd.DataFrame(all_festas, columns=columns)

output_csv = os.path.join(output_dir, 'todas_festas.csv')
df.to_csv(output_csv, index=False)

# Salvar as festas agrupadas por região em um JSON
output_json = os.path.join(output_dir, 'todas_festas.json')
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(all_festas, f, ensure_ascii=False, indent=4)

# Juntar as regioes com as festas
regioes = json.load(open('dados/regioes.json'))
festas = json.load(open('dados/todas_festas.json'))

# regioes
'''
[
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
                    },
'''

# festas
'''
[
    {
        "nome": "Cortejo dos Reis",
        "descricao": "Com pequeno auto teatral e leilão das ofertas",
        "data_inicio": "06/01/2024",
        "data_fim": null,
        "regiao": "beira_litoral",
        "distrito": "Aveiro",
        "concelho": "Sever do Vouga",
        "freguesia": "Talhadas",
        "festa_id": 1
    },
    {
        "nome": "Festa de S. Gonçalinho (S. Gonçalo de Amarante",
        "descricao": "Casamenteiro das velhas): junto à capela e do alto da mesma, lançamento de cavacas ao povo. Dança dos mancos, pequena comédia interpretada por homens. Música e danças pelas ruas.",
        "data_inicio": "10/01/2024",
        "data_fim": null,
        "regiao": "beira_litoral",
        "distrito": "Aveiro",
        "concelho": "Aveiro",
        "freguesia": null,
        "festa_id": 2
    },
    {
        "nome": "Festas de Nossa Senhora da Purificação e de S. Brás",
        "descricao": "Procissão das velas dedicada à Senhora da Purificação ou Senhora das Candeias, devoção muito expandida pelo país, cujo dia é o 2 de Fevereiro. Feira de gastronomia e dos grelos.",
        "data_inicio": "04/02/2024",
        "data_fim": null,
        "regiao": "beira_litoral",
        "distrito": "Aveiro",
        "concelho": "Vale de Cambra",
        "freguesia": "União das freguesias de Vila Chã, Codal e Vila Cova de Perrinho",
        "festa_id": 3
    },
'''

# Juntar da seguinte forma
'''
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
    ],
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
        }
    ]
}
'''

# Transformar o formato das festas conforme solicitado
formatted_festas = []
for festa in festas:
    formatted_festa = {
        "festa_id": festa["festa_id"],
        "nome": festa["nome"],
        "descricao": festa["descricao"],
        "data_inicio": festa["data_inicio"],
        "data_fim": festa["data_fim"] if festa["data_fim"] else festa["data_inicio"],
        "regiao": festa["regiao"],
        "distrito": festa["distrito"],
        "concelho": festa["concelho"],
        "freguesia": festa["freguesia"]
    }
    formatted_festas.append(formatted_festa)

# Juntar as regiões e festas no formato desejado
result = {
    "regioes": regioes,
    "festas": formatted_festas
}

# Guardar o resultado num ficheiro JSON
with open('dados/regioes_festas.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)