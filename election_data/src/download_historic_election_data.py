import os, wget, shutil, glob
from zipfile import ZipFile


def create_folders(paths):
    os.mkdir(paths['base'])
    for k, v in paths.items():
        if k != 'base':
            os.mkdir(v)

def get_links(years):
    links = []
    for year in years:
        if year < 1994:
            links.append(f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_candidato_uf/votacao_candidato_uf_{year}.zip')
        else:
            links.append(f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_{year}_BR.zip')
            links.append(f'http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{year}.zip')
    return links


def download(years, paths):
    create_folders(paths)

    # Download and extract right away
    for link in get_links(years):
        downloaded = wget.download(link, paths['zip'])
        print(downloaded)
        with ZipFile(downloaded, 'r') as zip:
            zip.extractall(paths['unzip'])
        print('unziped')

    ## Flat folder structure
    for file in glob.glob(f'{paths["unzip"]}/*/*.txt'):
        shutil.move(file, paths['unzip'])
