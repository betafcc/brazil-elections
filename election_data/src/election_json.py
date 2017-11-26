import os, glob, json

import pandas as pd


def find(arr, func):
    indexes = []
    for i, v in enumerate(arr):
        if func(v):
            indexes.append(i)
    return indexes


def load_data(ano):
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

    use = [
        'SIGLA_UF', 'NOME_URNA_CANDIDATO', 'DESCRICAO_CARGO',
        'NUM_TURNO', 'SIGLA_PARTIDO', 'TOTAL_VOTOS'
    ]

    path = f'../data/results_ALL/unzipped/{ano}/'
    all_files = glob.glob(os.path.join(path, '*.txt'))

    options = {
        'encoding': 'latin1',
        'sep': ';',
        'names': variaveis,
        'index_col': False,
        'usecols': use
    }

    df_from_each_file = (pd.read_csv(f, **options) for f in all_files)
    return pd.concat(df_from_each_file, ignore_index=True)

def filter_data(data, cargo, turno):
    final = data[
        (data.DESCRICAO_CARGO == cargo) &
        (data.NUM_TURNO == turno)
    ]
    del final['DESCRICAO_CARGO']
    del final['NUM_TURNO']

    return final

def mount_dic(data, ano, turno):
    final = {
        'ano': ano,
        'turno': turno,
        'candidatos': [],
        'estados': {}
    }

    g = data.groupby(['SIGLA_UF', 'SIGLA_PARTIDO', 'NOME_URNA_CANDIDATO'])
    s = g.TOTAL_VOTOS.sum()
    u = s.unstack('SIGLA_UF')

    it = u.transpose().sum().to_dict().items()
    for k, v in it:
        final['candidatos'].append({'partido': k[0], 'nome': k[1], 'votos': int(v)})
    final['candidatos'].sort(key=lambda x: x['votos'], reverse=True)


    for UF in u.keys():
        final['estados'][UF] = []
        r = final['estados'][UF]

        it = u[UF].to_dict().items()
        for k, v in it:
            r.append({
                'votos': int(v),
                'candidato': find(
                    final['candidatos'],
                    lambda x: x['nome'] == k[1]
                )[0]
            })
        r.sort(key=lambda x: x['votos'], reverse=True)

    return final

def to_json(dict):
    return json.dumps(dict, ensure_ascii=False)

def election_json(cargo, ano, turno):
    return to_json(mount_dic(filter_data(load_data(ano), cargo, turno), ano, turno))
