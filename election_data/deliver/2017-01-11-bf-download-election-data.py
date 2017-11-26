
# coding: utf-8

# In[1]:

import os, wget, shutil, glob
from zipfile import ZipFile


# In[5]:

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


# In[6]:

republica_nova = [1945, 1950, 1955, 1960]
regime_militar = [1964, 1966, 1969, 1974, 1978]
nova_republica = [1985, 1989, 1994, 1998, 2002, 2006, 2010, 2014]

YEARS = republica_nova + regime_militar + nova_republica
# 1985 foi indireta por decisão judicial 
DIRETAS = republica_nova + nova_republica[1:]


# In[7]:

base = '../data/results_ALL'
paths = {
    'base': base,
    'zip': f'{base}/zip',
    'unzip': f'{base}/unzip',
    'normalized': f'{base}/normalized',
    'json': f'{base}/json'
}


# In[8]:

create_folders(paths)


# In[10]:

# Download and extract right away
for link in get_links(DIRETAS):
    downloaded = wget.download(link, paths['zip'])
    print(downloaded)
    with ZipFile(downloaded, 'r') as zip:
        zip.extractall(paths['unzip'])
    print('unziped')


# In[23]:

## Flat folder structure
for file in glob.glob(f'{paths["unzip"]}/*/*.txt'):
    shutil.move(file, paths['unzip'])


# In[25]:

glob.glob(os.path.join(paths['unzip'], f'*{year}*.txt'))


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



