from collections import namedtuple

def not_in(arr, exclude):
    return [el for el in arr if el not in exclude]

def find(arr, func):
    return next((i, obj) for (i, obj) in enumerate(arr) if func(obj))

def find_val(arr, func):
    return find(arr, func)[1]

def find_index(arr, func):
    return find(arr, func)[0]


def gerar_nome_arquivo(ano, turno):
    return f'PRESIDENTE_{ano}_{turno}.json'

def options(**kwargs):
    return {
        'encoding': 'latin1',
        'sep': ';',
        'index_col': False,
        **kwargs
    }

def estruturar(ano, turno, candidatos, estados):
    return {
        'ano': ano,
        'turno': turno,
        'candidatos': candidatos,
        'estados': estados
    }

def candidatos(df):
    s = df.groupby(['NOME_CANDIDATO', 'SIGLA_PARTIDO']).TOTAL_VOTOS.sum()
    s = s.sort_values(ascending=False)

    candidatos = []
    for k, v in s.to_dict().items():
            candidatos.append({'nome': k[0], 'partido': k[1], 'votos': int(v)})
    candidatos.sort(key=lambda el: el['votos'], reverse=True)
    return candidatos

def estados(df, candidatos):
    s = df.groupby(['SIGLA_UF', 'NOME_CANDIDATO']).TOTAL_VOTOS.sum()
    dic = s.to_dict()

    # cria dicionario incializado com lista
    # vazia pra cada estado
    estados = {}
    for estado in set([i[0] for i in list(dic)]):
        estados[estado] = []

    # popula a lista para cada estado
    for (estado, candidato), votos in dic.items():
        estados[estado].append({
                'candidato': find_index(
                    candidatos,
                    lambda el: el['nome'] == candidato
                ),
                'votos': int(votos)})

    # ordena por mais votado em cada estado 
    for estado in estados.values():
        estado.sort(key=lambda el: el['votos'], reverse=True)

    return estados

def get_eleicoes():
    Eleicao = namedtuple('Eleicao', ['ano', 'turno'])

    republica_nova = [1945, 1950, 1955, 1960]
    regime_militar = [1964, 1966, 1969, 1974, 1978]
    nova_republica = [1985, 1989, 1994, 1998, 2002, 2006, 2010, 2014]

    todas = republica_nova + regime_militar + nova_republica
    diretas = republica_nova + nova_republica[1:]

    turnos = map(
        lambda x: [*range(1, x + 1)],
        [1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2]
    )
    ano_turnos = [*zip(diretas, turnos)]

    eleicoes = []
    for eleicao in ano_turnos:
        for turno in eleicao[1]:
            eleicoes.append(Eleicao(eleicao[0], turno))

    return (eleicoes, ano_turnos)

eleicoes, ano_turnos = get_eleicoes()

postals = {
    'Brasil': 'BR',
    'Exterior': 'ZZ',

    'Acre' : 'AC',
    'Alagoas' : 'AL',
    'Amapá' : 'AP',
    'Amazonas' : 'AM',
    'Bahia' : 'BA',
    'Ceará' : 'CE',
    'Distrito Federal' : 'DF',
    'Espírito Santo' : 'ES',
    'Goiás' : 'GO',
    'Maranhão' : 'MA',
    'Mato Grosso' : 'MT',
    'Mato Grosso do Sul' : 'MS',
    'Minas Gerais' : 'MG',
    'Pará' : 'PA',
    'Paraíba' : 'PB',
    'Paraná' : 'PR',
    'Pernambuco' : 'PE',
    'Piauí' : 'PI',
    'Rio de Janeiro' : 'RJ',
    'Rio Grande do Norte' : 'RN',
    'Rio Grande do Sul' : 'RS',
    'Rondônia' : 'RO',
    'Roraima' : 'RR',
    'Santa Catarina' : 'SC',
    'São Paulo' : 'SP',
    'Sergipe' : 'SE',
    'Tocantins' : 'TO',


    'Brasília': 'DF',

    'Guanabara': 'GB',

    'Território De Rondônia' : 'RO',
    'Território de Rondônia': 'RO',
    'Território de Roraima': 'RR',
    'Território do Acre': 'AC',
    'Território do Amapá': 'AP',
    'Território do Guaporé': 'GP',
    'Território do Rio Branco': 'RB'
}