import pandas as pd

VARIAVEIS_VOTACAO_CANDIDATO_UF = [
    'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
    'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
    'SIGLA_UE', 'CODIGO_CARGO', 'NUMERO_CAND',
    'SQ_CANDIDATO', 'NOME_CANDIDATO', 'NOME_URNA_CANDIDATO',
    'DESCRICAO_CARGO', 'COD_SIT_CAND_SUPERIOR', 'DESC_SIT_CAND_SUPERIOR',
    'CODIGO_SIT_CANDIDATO', 'DESC_SIT_CANDIDATO', 'CODIGO_SIT_CAND_TOT',
    'DESC_SIT_CAND_TOT', 'NUMERO_PARTIDO', 'SIGLA_PARTIDO',
    'NOME_PARTIDO', 'SEQUENCIAL_LEGENDA', 'NOME_COLIGACAO',
    'COMPOSICAO_LEGENDA', 'TOTAL_VOTOS'
]

VARIAVEIS_VOTO_SECAO = [
    'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
    'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
    'SIGLA_UE', 'CODIGO_MUNICIPIO', 'NOME_MUNICIPIO',
    'NUM_ZONA', 'NUM_SECAO', 'CODIGO_CARGO',
    'DESCRICAO_CARGO', 'NUM_VOTAVEL', 'QTDE_VOTOS'
]


def get_columns_names(year):
    check_year(year)
    if year < 1994:
        return VARIAVEIS_VOTACAO_CANDIDATO_UF
    else:
        return VARIAVEIS_VOTO_SECAO

def get_folder(year):
    return f'{path_unzipped}/{year}'

def get_files(year):
    return glob.glob(f'{get_folder(year)}/*.txt')


def parse_file(file, year):
    options = {
        'encoding': 'latin1',
        'sep': ';',
        'names': get_columns_names(year),
        'index_col': False
    }
    
    return pd.read_csv(file, **options)