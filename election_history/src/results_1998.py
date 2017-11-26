import requests
import pandas as pd
import os

from bs4 import BeautifulSoup as BS

from .utils import postals, find_index, estruturar

def preparar(ano=None):
    folder = f'../data/working/{ano}'
    url_parent = 'https://pt.wikipedia.org/wiki/Elei%C3%A7%C3%A3o_presidencial_no_Brasil_em_1998'

    os.mkdir(folder)

    
    r = requests.get(url_parent)

    with open(f'{folder}/results.html', 'w') as f:
        f.write(r.text)

    print('Sucess!')

def carregar(ano):
    folder = f'../data/working/{ano}'

    with open(f'{folder}/results.html', 'r') as f:
        soup = BS(f.read(), 'html.parser')

    return soup
    
def candidatos(soup):
    s = soup.select('#Resultado')[0]
    table = s.find_all_next('table')[0]


    s = pd.read_html(str(table))[0]

    s.columns = s.iloc[0]
    s = s.drop(0)
    s = s.drop(['Imagem', 'Vice', 'Coligação', '%'], axis=1)

    s.Votos = s.Votos.str.replace('.', '')
    s.Votos = pd.to_numeric(s.Votos)

    s['SIGLA_PARTIDO'] = s.Candidato.str.extract(r'\((\w+)\)', expand=False)
    s['NOME_CANDIDATO'] = s.Candidato.str.extract(r'(.+) \(', expand=False)
    s['TOTAL_VOTOS'] = s.Votos


    df = s.drop(['Candidato', 'Votos'], axis=1)
    s = df.groupby(['NOME_CANDIDATO', 'SIGLA_PARTIDO']).TOTAL_VOTOS.sum()
    s = s.sort_values(ascending=False)

    candidatos = []
    for k, v in s.to_dict().items():
            candidatos.append({'nome': k[0], 'partido': k[1], 'votos': int(v)})
    candidatos.sort(key=lambda el: el['votos'], reverse=True)
    return candidatos

# estados
def estados(soup, candidatos):
    s = soup.select('#Resultados_por_estados')[0]
    table = s.find_all_next('table')[1]

    s = pd.read_html(str(table), header=[0, 1])[0]

    mlti = pd.MultiIndex(levels=[[
                'State',
                'Fernando Henrique Cardoso',
                'Luiz Inácio Lula da Silva',
                'Ciro Gomes',
                'Outros vários',
                'Margem',
                'Total',
    ], ['#', '%', 'Nome']], labels=[[0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6],
                            [2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]])

    s.columns = mlti
    s = s.drop([column for column in s.columns if column[1] == '%'], axis=1)
    s.columns = s.columns.levels[0]
    s.State = s.State.map(lambda uf: postals[uf])
    s = s.drop(['Outros vários', 'Margem', 'Total'], axis=1)
    t = s.transpose()
    t.columns = t.iloc[0]
    t = t.drop(['State'], axis=0)


    estados = t.to_dict()
    for k in estados:
        estados[k] = list(estados[k].items())
        estados[k] = [{
                    'candidato': find_index(
                        candidatos,
                        lambda el: el['nome'] == val[0]
                    ),
                    'votos': int(val[1].replace('.', ''))
                  } for val in estados[k]]

    # ordena por mais votado em cada estado 
    for estado in estados.values():
        estado.sort(key=lambda el: el['votos'], reverse=True)

    return estados

def resultados_turnos(ano, turnos):
    try:
        preparar(ano)
    except:
        pass
    
    soup = carregar(ano)
    
    resultados = []
    for turno in turnos:
        cand = candidatos(soup)
        estd = estados(soup, cand)
        
        resultados.append(estruturar(ano, turno, cand, estd))
    
    return resultados
