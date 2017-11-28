from .util import DATA_ROOT, absjoin, load_json, to_json
from .download_thumbnails import INDEX as INDEX_SRC
from .extrair_candidatos import SRC as CANDIDATOS_SRC


DEST = absjoin(DATA_ROOT, 'deliver', 'elections.json')


if __name__ == '__main__':
    elections  = load_json(CANDIDATOS_SRC)
    nome_img   = load_json(INDEX_SRC)


    for election in elections:
        for candidato in election['candidatos']:
            try:
                candidato['imgSrc'] = nome_img[candidato['nome']]
            except KeyError:
                pass

    to_json(elections, DEST, minify=True)
