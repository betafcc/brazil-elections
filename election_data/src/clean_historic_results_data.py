import os
import glob
import pandas as pd


def load_data(year, paths):
    if year < 1994:
        files_pattern = f'*{year}*.txt'
        variaveis = [
            'DATA_GERACAO',
            'HORA_GERACAO',
            'ANO_ELEICAO',
            'NUM_TURNO',
            'DESCRICAO_ELEICAO',
            'SIGLA_UF',
            'SIGLA_UE',
            'CODIGO_CARGO',
            'NUMERO_CAND',
            'SQ_CANDIDATO',
            'NOME_CANDIDATO',
            'NOME_URNA_CANDIDATO',
            'DESCRICAO_CARGO',
            'COD_SIT_CAND_SUPERIOR',
            'DESC_SIT_CAND_SUPERIOR',
            'CODIGO_SIT_CANDIDATO',
            'DESC_SIT_CANDIDATO',
            'CODIGO_SIT_CAND_TOT',
            'DESC_SIT_CAND_TOT',
            'NUMERO_PARTIDO',
            'SIGLA_PARTIDO',
            'NOME_PARTIDO',
            'SEQUENCIAL_LEGENDA',
            'NOME_COLIGACAO',
            'COMPOSICAO_LEGENDA',
            'TOTAL_VOTOS'
        ]

        use = [
            'SIGLA_UF',
            'NOME_URNA_CANDIDATO',
            'NOME_CANDIDATO',
            'DESCRICAO_CARGO',
            'NUM_TURNO',
            'SIGLA_PARTIDO',
            'TOTAL_VOTOS'
        ]

    else:
        files_pattern = f'votacao_secao_{year}*.txt'
        variaveis = [
            'DATA_GERACAO',
            'HORA_GERACAO',
            'ANO_ELEICAO',
            'NUM_TURNO',
            'DESCRICAO_ELEICAO',
            'SIGLA_UF',
            'SIGLA_UE',
            'CODIGO_MUNICIPIO',
            'NOME_MUNICIPIO',
            'NUM_ZONA',
            'NUM_SECAO',
            'CODIGO_CARGO',
            'DESCRICAO_CARGO',
            'NUM_VOTAVEL',
            'QTDE_VOTOS'
        ]

        use = [
            'SIGLA_UF',
            'NUM_VOTAVEL',
            'DESCRICAO_CARGO',
            'NUM_TURNO',
            'QTDE_VOTOS'
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


def generate_results_frame(year, turno, cargo, paths):
    df = load_data(year, paths)
    df = df[df.DESCRICAO_CARGO == cargo]
    df = df[df.NUM_TURNO == turno]

    if year < 1994:
        df = df[['SIGLA_UF', 'NOME_URNA_CANDIDATO', 'TOTAL_VOTOS']]

        df = df.groupby(['SIGLA_UF', 'NOME_URNA_CANDIDATO']).sum()
        df.TOTAL_VOTOS = df.TOTAL_VOTOS.map(lambda x: int(x))
        df = df.unstack('SIGLA_UF')
        df.columns = df.columns.droplevel()

    else:
        df = df[['SIGLA_UF', 'NUM_VOTAVEL', 'QTDE_VOTOS']]
        # TODO: load consulta candidato do ano e
        # substituir NUM_VOTAL por NOME URNA

        df = df.groupby(['SIGLA_UF', 'NUM_VOTAVEL']).sum()
        df.TOTAL_VOTOS = df.QTDE_VOTOS.map(lambda x: int(x))
        df = df.unstack('SIGLA_UF')
        df.columns = df.columns.droplevel()      

        return df

    # options = {
    #     'encoding': 'latin1',
    #     'sep': ';',
    #     # 'index': False,
    # }

    # filepath = os.path.join(paths['normalized'], f'{cargo}_{year}_{turno}.txt')
    # with open(filepath, 'w') as file:
    #     df.to_csv(file, **options)

    # return filepath
