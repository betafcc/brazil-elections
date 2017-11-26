
# coding: utf-8

# # All Presidential election results from 1945 to 2014

# ## This notebook aims to:
#     - [X] Find all the years that had presidential elections
#     - [X] Find the data of all of them
#     - [X] develop a script to download them all

# ## Notas:
#     - Os únicos dados providos pelo tse, são referentes às 
#     eleições diretas no período 1945-Atual, excluindo então
#     o período de ditadura e a primeira da nova república

# In[2]:

from IPython.display import IFrame


# # Ache todos os anos que tiveram eleições presidenciais

# In[3]:

IFrame(
    'https://pt.wikipedia.org/wiki/Lista_de_elei%C3%A7%C3%B5es_presidenciais_no_Brasil#toc',
    800, 600
)


# ## Copie os que o TSE possui dados

# In[4]:

republica_nova = [1945, 1950, 1955, 1960]
regime_militar = [1964, 1966, 1969, 1974, 1978]
nova_republica = [1985, 1989, 1994, 1998, 2002, 2006, 2010, 2014]

YEARS = republica_nova + regime_militar + nova_republica
# 1985 foi indireta por decisão judicial 
DIRETAS = republica_nova + nova_republica[1:]
print(YEARS)
print(DIRETAS)


# ## Ache os dados de todos

# In[5]:

IFrame(
    'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/1945.html',
    800, 400
)


# A regra é 'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/' + < ano > + '.html'

# In[6]:

def check_year(year):
    if year not in DIRETAS:
        raise ValueError(f'year {year} had no presidential election')
    else:
        return True


# In[7]:

def election_page(year):
    check_year(year)
    return f'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/{year}.html'


# In[8]:

# exemplo:
IFrame(
    election_page(DIRETAS[-2]), # penultima eleições
    800, 400
)


# ## Ache o link direto para o arquivo zip de cada

# In[9]:

def election_data(year):
    check_year(year)
    if year < 1994:
        return f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_candidato_uf/votacao_candidato_uf_{year}.zip'
    else:
        return f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_{year}_BR.zip'


# ### Check the response of the links

# In[10]:

import requests


# In[11]:

for year in DIRETAS:
    link = election_data(year)
    req = requests.get(link)
    print(link)
    print(req)


# ## Faça o download de todos

# In[12]:

import os


# In[13]:

base_path = '../data/results_ALL'
# os.mkdir(base_path)


# In[14]:

path_zipped  = f'{base_path}/zipped'
path_unzipped = f'{base_path}/unzipped'

# os.mkdir(path_zipped)
# os.mkdir(path_unzipped)


# In[15]:

# import wget

# for year in DIRETAS:
#     result = wget.download(election_data(year), path_zipped)
#     print(result)


# In[16]:

os.listdir(path_zipped)


# ## Unzipe todos

# In[27]:

from zipfile import ZipFile


# In[28]:

paths = [f'{path_zipped}/{file}' for file in os.listdir(path_zipped)]


# In[29]:

import re


# In[32]:

os.mkdir(path_unzipped)
for zip_file_path in paths:
    with ZipFile(zip_file_path, 'r') as file:
        year = re.findall(r"\d+", zip_file_path)[0]
        folder = f'{path_unzipped}/{year}'
        os.mkdir(folder)
        file.extractall(folder)


# In[33]:

os.listdir(path_unzipped)


# ### Existe uma pequena inconsistencia dos arquivos antes de 1994, eles estão nested num folder, as seguintes linhas padroniza isso:

# In[34]:

import glob


# In[35]:

import shutil

for year_folder in os.listdir(path_unzipped):
    if int(year_folder) < 1994:
        print(year_folder)
        nested_folder = glob.glob(f'{path_unzipped}/{year_folder}/*')[0] 
        for file in glob.glob(f'{nested_folder}/*'):
            shutil.move(file, f'{path_unzipped}/{year_folder}/')
        os.rmdir(nested_folder)


# In[36]:

len(glob.glob(f'{path_unzipped}/**/*'))


# ## Script criado em ../src/download-historic-election-data.py

# In[ ]:



