import os
import shutil
import wget
import pandas as pd
import requests
from bs4 import BeautifulSoup as BS
from glob import glob
from zipfile import ZipFile

from .utils import *
from .tabelas import tabela_consulta_cand, tabela_voto_secao

def preparar(ano):
    folder = f'../data/working/{ano}'
    folder_candidatos = f'{folder}/candidatos'
    folder_resultados = f'{folder}/resultados'

    url_candidatos = f'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip'

    r = requests.get(f'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/votacao/votacao_secao_eleitoral_{ano}.html')

    soup = BS(r.text, 'html.parser')
    anchors = soup.select('p > a')

    urls_resultados = [a.attrs['href'] for a in anchors]
    print(urls_resultados)

    for f in [folder, folder_candidatos, folder_resultados]:
        os.mkdir(f)

    print('Downloading...')
    zip_candidatos = wget.download(url_candidatos, folder_candidatos)

    ## download all links
    for url in urls_resultados:
        print(url)
        wget.download(url, folder_resultados)
    
    print('Extracting')
    with ZipFile(zip_candidatos, 'r') as zip:
        zip.extractall(folder_candidatos)

    for zip_full_path in glob(f'{folder_resultados}/*.zip'):
        with ZipFile(zip_full_path, 'r') as zip:
            zip.extractall(folder_resultados)

    print('Sucess!')


def carregar(ano):
    ## Carregue candidatos
    names = tabela_consulta_cand(ano)
    usecols = [
        'NUM_TURNO',
        'DESCRICAO_CARGO',
        'NUMERO_CANDIDATO',
        'NOME_CANDIDATO',
        'SIGLA_PARTIDO'
    ]
    opts = options(names=names, usecols=usecols)
    files = glob(f'../data/working/{ano}/candidatos/*.txt')
    df_cand = (pd.read_csv(file,**opts) for file in files)

    df_cand = pd.concat(df_cand, ignore_index=True)

    df_cand = df_cand[df_cand.DESCRICAO_CARGO == 'PRESIDENTE']
    df_cand = df_cand.drop('DESCRICAO_CARGO', axis=1)

    ## Carregue votos
    names = tabela_voto_secao()
    usecols = [
        'NUM_TURNO',
        'SIGLA_UF',
        'DESCRICAO_CARGO',
        'NUM_VOTAVEL',
        'QTDE_VOTOS'
    ]
    opts = options(names=names, usecols=usecols)
    files = glob(f'../data/working/{ano}/resultados/*.txt')
    files = [file for file in files if file[-6:-4] != 'BR']
    # print(files)

    df_vot = (
        [
            (lambda df:
                df[df.DESCRICAO_CARGO == 'PRESIDENTE'].drop('DESCRICAO_CARGO', axis=1)
            )(pd.read_csv(file,**opts)),
            print(file)
        ][0] for file in files)

    print('Loading...')
    df_vot = pd.concat(df_vot, ignore_index=True)

    # df_vot = df_vot[df_vot.DESCRICAO_CARGO == 'PRESIDENTE']
    # df_vot = df_vot.drop('DESCRICAO_CARGO', axis=1)

    ## As tabelas parecem tá bugadas, então double check com dos candidatos
    numeros_validos = df_cand.NUMERO_CANDIDATO.unique()
    print('Filtering...')
    df_vot = df_vot[df_vot.NUM_VOTAVEL.map(lambda num: num in numeros_validos)]

    # return df_vot
    print('Transforming...')
    df_vot.rename(columns={'QTDE_VOTOS': 'TOTAL_VOTOS'}, inplace=True)

    nome_partido = nome_partido_memo()
    nomes_partidos = df_vot.NUM_VOTAVEL.map(lambda num: nome_partido(df_cand, num))

    df_vot.drop('NUM_VOTAVEL', axis=1, inplace=True)
    df_vot['NOME_CANDIDATO'] = nomes_partidos.map(lambda el: el[0])
    df_vot['SIGLA_PARTIDO'] = nomes_partidos.map(lambda el: el[1])

    return df_vot



def nome_partido_memo():
    memo = {}
    def nome_partido(df_cand, numero):
        if numero in memo:
            return memo[numero]

        cand =  df_cand[df_cand.NUMERO_CANDIDATO == numero]
        memo[numero] = (cand.NOME_CANDIDATO.iloc[0], cand.SIGLA_PARTIDO.iloc[0])

        return memo[numero]
    return nome_partido

# Carrega a dataframe de um ano
# pra apenas um turno mesmo que o
# ano tenha dois
def resultado(ano, turno):
    try:
        preparar(ano)
    except:
        pass

    df = carregar(ano)

    f = df[df.NUM_TURNO == turno]
    cand = candidatos(f)
    estd = estados(f, cand)

    return estruturar(ano, turno, cand, estd)


# Mais eficiente, só carrega a dataframe
# de um certo ano uma vez mesmo que tenha
# mais de um turno
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

