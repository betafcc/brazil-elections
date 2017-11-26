import os, glob
import pandas as pd


def load_data(year, paths):
    if year < 1994:
        files_pattern = f'*{year}*.txt'
        variaveis = [
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

    elif year <= 2010:
        files_pattern = f'consulta_cand_{year}*.txt'
        variaveis = [
            'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
            'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
            'SIGLA_UE', 'DESCRICAO_UE', 'CODIGO_CARGO',
            'DESCRICAO_CARGO', 'NOME_CANDIDATO', 'SEQUENCIAL_CANDIDATO',
            'NUMERO_CANDIDATO', 'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
            'COD_SITUACAO_CANDIDATURA', 'DES_SITUACAO_CANDIDATURA', 'NUMERO_PARTIDO',
            'SIGLA_PARTIDO', 'NOME_PARTIDO', 'CODIGO_LEGENDA',
            'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA', 'NOME_LEGENDA',
            'CODIGO_OCUPACAO', 'DESCRICAO_OCUPACAO', 'DATA_NASCIMENTO',
            'NUM_TITULO_ELEITORAL_CANDIDATO', 'IDADE_DATA_ELEICAO', 'CODIGO_SEXO',
            'DESCRICAO_SEXO', 'COD_GRAU_INSTRUCAO', 'DESCRICAO_GRAU_INSTRUCAO',
            'CODIGO_ESTADO_CIVIL', 'DESCRICAO_ESTADO_CIVIL', 'CODIGO_NACIONALIDADE',
            'DESCRICAO_NACIONALIDADE', 'SIGLA_UF_NASCIMENTO', 'CODIGO_MUNICIPIO_NASCIMENTO',
            'NOME_MUNICIPIO_NASCIMENTO', 'DESPESA_MAX_CAMPANHA', 'COD_SIT_TOT_TURNO',
            # 'DESC_SIT_TOT_TURNO'
        ]
    
    elif year == 2012:
        files_pattern = f'consulta_cand_{year}*.txt'
        variaveis = [
            'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
            'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
            'SIGLA_UE', 'DESCRICAO_UE', 'CODIGO_CARGO',
            'DESCRICAO_CARGO', 'NOME_CANDIDATO', 'SEQUENCIAL_CANDIDATO',
            'NUMERO_CANDIDATO', 'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
            'COD_SITUACAO_CANDIDATURA', 'DES_SITUACAO_CANDIDATURA', 'NUMERO_PARTIDO',
            'SIGLA_PARTIDO', 'NOME_PARTIDO', 'CODIGO_LEGENDA',
            'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA', 'NOME_LEGENDA',
            'CODIGO_OCUPACAO', 'DESCRICAO_OCUPACAO', 'DATA_NASCIMENTO',
            'NUM_TITULO_ELEITORAL_CANDIDATO', 'IDADE_DATA_ELEICAO', 'CODIGO_SEXO',
            'DESCRICAO_SEXO', 'COD_GRAU_INSTRUCAO', 'DESCRICAO_GRAU_INSTRUCAO',
            'CODIGO_ESTADO_CIVIL', 'DESCRICAO_ESTADO_CIVIL', 'CODIGO_NACIONALIDADE',
            'DESCRICAO_NACIONALIDADE', 'SIGLA_UF_NASCIMENTO', 'CODIGO_MUNICIPIO_NASCIMENTO',
            'NOME_MUNICIPIO_NASCIMENTO', 'DESPESA_MAX_CAMPANHA', 'COD_SIT_TOT_TURNO',
            'DESC_SIT_TOT_TURNO', 'NM_EMAIL'
        ]
    
    elif year >= 2014:
        files_pattern = f'consulta_cand_{year}*.txt'
        variaveis = [
            'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
            'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
            'SIGLA_UE', 'DESCRICAO_UE', 'CODIGO_CARGO',
            'DESCRICAO_CARGO', 'NOME_CANDIDATO', 'SEQUENCIAL_CANDIDATO',
            'NUMERO_CANDIDATO', 'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
            'COD_SITUACAO_CANDIDATURA', 'DES_SITUACAO_CANDIDATURA', 'NUMERO_PARTIDO',
            'SIGLA_PARTIDO', 'NOME_PARTIDO', 'CODIGO_LEGENDA',
            'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA', 'NOME_LEGENDA',
            'CODIGO_OCUPACAO', 'DESCRICAO_OCUPACAO', 'DATA_NASCIMENTO',
            'NUM_TITULO_ELEITORAL_CANDIDATO', 'IDADE_DATA_ELEICAO', 'CODIGO_SEXO',
            'DESCRICAO_SEXO', 'COD_GRAU_INSTRUCAO', 'DESCRICAO_GRAU_INSTRUCAO',
            'CODIGO_ESTADO_CIVIL', 'DESCRICAO_ESTADO_CIVIL', 'CODIGO_COR_RACA',
            'DESCRICAO_COR_RACA', 'CODIGO_NACIONALIDADE', 'DESCRICAO_NACIONALIDADE',
            'SIGLA_UF_NASCIMENTO', 'CODIGO_MUNICIPIO_NASCIMENTO', 'NOME_MUNICIPIO_NASCIMENTO',
            'DESPESA_MAX_CAMPANHA', 'COD_SIT_TOT_TURNO', 'DESC_SIT_TOT_TURNO',
            'NM_EMAIL'
        ]
        
    use = [
        'SIGLA_UF', 'NOME_URNA_CANDIDATO', 'NOME_CANDIDATO', 'DESCRICAO_CARGO',
        'NUM_TURNO', 'SIGLA_PARTIDO'
    ]

    all_files = glob.glob(os.path.join(paths['unzip'], files_pattern))

    options = {
        'encoding': 'latin1',
        'sep': ';',
        'names': variaveis,
        'index_col': False,
        'usecols': use
    }

    df_from_each_file = (pd.read_csv(f, **options) for f in all_files)
    return pd.concat(df_from_each_file, ignore_index=True)


def generate_candidatos_frame(year, cargo, paths):
    df = load_data(year, paths)
    df = df[df.DESCRICAO_CARGO == cargo]
    df = df[['NOME_CANDIDATO', 'NOME_URNA_CANDIDATO', 'SIGLA_PARTIDO']]
    df = df.drop_duplicates()

    options = {
        'encoding': 'latin1',
        'sep': ';',
        'index': False,
    }

    filepath = os.path.join(paths['normalized'], f'CANDIDATOS_{cargo}_{year}.txt')
    with open(filepath, 'w') as file:
        df.to_csv(file, **options)

    return filepath