import os
import shutil
import wget
import pandas as pd
from glob import glob
from zipfile import ZipFile

from .utils import *
from .tabelas import tabela_votacao_candidato

def preparar(ano):
    folder = f'../data/working/{ano}'
    url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_candidato_uf/votacao_candidato_uf_{ano}.zip'

    os.mkdir(folder)

    print('Downloading...')
    f = wget.download(url, folder)

    print('Extracting')
    with ZipFile(f, 'r') as zip:
        zip.extractall(folder)
    
    print('Moving...')
    for file in glob(f'{folder}/*/*'):
        shutil.move(file, folder)

    print('Sucess!')

def carregar(ano):
    folder = f'../data/working/{ano}'
    names = tabela_votacao_candidato()

    usecols = [
        'NUM_TURNO',
        'SIGLA_UF',
        'NOME_CANDIDATO',
        'DESCRICAO_CARGO',
        'SIGLA_PARTIDO',
        'TOTAL_VOTOS',
    ]

    opts = options(names=names, usecols=usecols)
    
    files = glob(os.path.join(folder, '*.txt'))
    df = (pd.read_csv(file, **opts) for file in files)

    df = pd.concat(df, ignore_index=True)

    df = df[df.DESCRICAO_CARGO == 'PRESIDENTE']
    df = df.drop('DESCRICAO_CARGO', axis=1)

    return df

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


def main():
    resultados = (eleicao for eleicao in eleicoes if eleicao.ano <= 1989)
    resultados = (resultado(eleicao.ano, eleicao.turno) for eleicao in resultados)

    return list(resultados)
