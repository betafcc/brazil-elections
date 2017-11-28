from .util import to_json, load_json, absjoin, DATA_ROOT


SRC  = absjoin(DATA_ROOT, 'raw', 'elections.json')
DEST = absjoin(DATA_ROOT, 'interim', 'candidatos.json')


if __name__ == '__main__':
    elections = load_json(SRC)

    candidatos = {
        candidato['nome']: None
        for election in elections
        for candidato in election['candidatos']
    }


    to_json(candidatos, DEST)
