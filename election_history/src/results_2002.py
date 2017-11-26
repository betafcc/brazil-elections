import os
import shutil
import wget
import pandas as pd
from glob import glob
from zipfile import ZipFile

from .utils import *
from .tabelas import tabela_votacao_candidato_munzona

def preparar(ano):
    folder = f'../data/working/{ano}'
    folder_candidatos = f'{folder}/candidatos'
    folder_resultados = f'{folder}/resultados'

    url_candidatos = f'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip'
    url_resultados = f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip'

    for f in [folder, folder_candidatos, folder_resultados]:
        os.mkdir(f)

    print('Downloading...')
    zip_candidatos = wget.download(url_candidatos, folder_candidatos)
    wget.download(url_resultados, folder_resultados)
    
    print('Extracting')
    with ZipFile(zip_candidatos, 'r') as zip:
        zip.extractall(folder_candidatos)

    for zip_full_path in glob(f'{folder_resultados}/*.zip'):
        with ZipFile(zip_full_path, 'r') as zip:
            zip.extractall(folder_resultados)

    print('Sucess!')


def carregar(ano):
    ## Carregue votos
    names = tabela_votacao_candidato_munzona(ano)
    usecols = [
        'NUM_TURNO',
        'SIGLA_UF',
        'DESCRICAO_CARGO',
        'NOME_CANDIDATO',
        'SIGLA_PARTIDO',
        'TOTAL_VOTOS'
    ]
    opts = options(names=names, usecols=usecols)
    files = glob(f'../data/working/{ano}/resultados/*.txt')
    files = [file for file in files if file[-6:-4] in ['BR', 'ZZ', 'VT']]
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
    return df_vot


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

