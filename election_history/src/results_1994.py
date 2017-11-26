import os
import requests
import pandas as pd

from glob import glob
from collections import namedtuple
from bs4 import BeautifulSoup as BS 

from .utils import *
from .tabelas import tabela_votacao_estados

def structure_table(table):
    structured = []
    rows = table.data.select('tr')

    while len(rows[0].select('th')) == 0:
        del rows[0]

    header, data = rows[0], rows[1:]
    header = tabela_votacao_estados() + ['VALIDOS']

    structured.append(header)
    for dr in data:
        structured.append([1, table.UF] + [next(td.strings) for td in dr.select('td')])

    return structured


def preparar(ano):
    folder = f'../data/working/{ano}'
    url_parent = 'http://www.tse.jus.br/eleicoes/eleicoes-anteriores/eleicoes-1994/resultados-das-eleicoes-1994'

    os.mkdir(folder)

    Resultado = namedtuple('Resultado', ['UF', 'data'])

    print('Começando o scrapping...')
    r = requests.get(url_parent)
    soup = BS(r.text, 'html.parser')    

    hrefs = soup.select('tr.tabelas a')
    hrefs = [(list(a.strings)[0], a.attrs['href']) for a in hrefs]
    hrefs = [Resultado(postals[uf], href) for uf, href in hrefs if uf != 'Brasil']


    print('Pegando página de resultados...')
    hrefs_results = []
    for uf, href in hrefs:
        r = requests.get(href)
        soup = BS(r.text, 'html.parser')
        print(uf, end=' ')
        url_results = soup.find(text='Presidente').parent.attrs['href']

        hrefs_results.append(Resultado(uf, url_results))
    print('')


    print('Pegando Tabelas...')
    tables_results = []
    for uf, href in hrefs_results:
        r = requests.get(href)
        soup = BS(r.text, 'html.parser')
        print(uf, end=' ')
        table = soup.select('table')[0]
        
        tables_results.append(Resultado(uf, table))
    print('')

    print('Formatando...')
    tables = [structure_table(table) for table in tables_results]
    df = pd.concat((pd.DataFrame(table[1:], columns=table[0]) for table in tables), ignore_index=True)

    print('Filtrando...')
    df.NOME_CANDIDATO = df.NOME_CANDIDATO.str.slice(3)
    df = df.drop('VALIDOS', axis=1)

    df.TOTAL_VOTOS = df.TOTAL_VOTOS.str.replace('.', '')

    print('Escrevendo csv...')
    df.to_csv(
        f'{folder}/votacao_estados.txt',
        sep=';',
        encoding='latin1',
        index=False,
        header=False,
    )
    print('Feito')

def carregar(ano):
    folder = f'../data/working/{ano}'
    names = tabela_votacao_estados()

    opts = options(names=names)
    
    files = glob(os.path.join(folder, '*.txt'))
    df = (pd.read_csv(file, **opts) for file in files)

    return pd.concat(df, ignore_index=True)


def resultado(ano, turno):
    print(f'{ano}, {turno}')

    try:
        preparar(ano)
    except:
        pass

    df = carregar(ano)

    f = df[df.NUM_TURNO == turno]
    cand = candidatos(f)
    estd = estados(f, cand)

    return estruturar(ano, turno, cand, estd)

def resultados_turnos(ano, turnos):
    print(f'{ano}, {turnos}')

    try:
        preparar(ano)
    except:
        pass

    df = carregar(ano)

    resultados = []
    for turno in turnos:
        f = df[df.NUM_TURNO == turno]
        cand = candidatos(f)
        estd = estados(f, cand)

        resultados.append(estruturar(ano, turno, cand, estd))

    return resultados
