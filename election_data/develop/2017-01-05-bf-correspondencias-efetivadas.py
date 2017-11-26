
# coding: utf-8

# # Correspondências Efetivadas

# ## This notebook aims to:
#     - [X] Achar links dos arquivos de correspondências efetivadas
#     - [X] Baixar automatizadamente todos
#     - [X] Explorar

# In[1]:

from IPython.display import IFrame


# ## Ache a página com os resultados da última eleição para presidente

# In[39]:

IFrame(
    'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/2014.html',
    600, 400
)


# ## Faça download dos dados nacionais das correspondências efetivas de segundo turno

#     - [X] Mostre a página
#     - [X] Carrege a página com os links via requests
#     - [X] Scrape a página com BeautifulSoup pra pegar os links
#     - [X] Faça download de todos

# In[43]:

IFrame(
    'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/tabela_correspondencia/2014/correspondencias_efetivadas_2_turno.html',
    600, 400
)


# In[42]:

import requests


# In[47]:

url = 'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/tabela_correspondencia/2014/correspondencias_efetivadas_2_turno.html'
r = requests.get(url)
r.status_code


# In[51]:

from bs4 import BeautifulSoup as BS


# In[113]:

# Pegue os 'li' que contém tanto a UF quanto o link pro arquivo
soup = BS(r.content, 'html.parser')
links = soup.select_one('#tabela_correspondencia')
links = links.select('li')


# In[114]:

# formate para lista de {UF, href}
UFS = [next(link.stripped_strings) for link in links]
hrefs = [link.select('a')[0].attrs['href'] for link in links]
links = [{'UF': UF, 'href': href} for (UF, href) in zip(UFS, hrefs)]
links[0:5]


# In[127]:

import wget
from os import mkdir, listdir


# In[143]:

zip_folder   = '../data/ceft_2t_TODOS_2014_ZIP'
unzip_folder = '../data/ceft_2t_TODOS_2014_UNZIP'


# In[124]:

# mkdir(zip_folder)
# for link in links:
#     wget.download(link['href'], out=zip_folder)
#     print(f'{link["UF"]} done')


# In[140]:

zip_names = listdir(zip_folder)
zip_names


# In[141]:

zip_paths = [f'{folder}/{file}' for file in zip_names]


# In[142]:

from zipfile import ZipFile


# In[148]:

for path in zip_paths:
    with ZipFile(path, 'r') as file:
        file.extractall(unzip_folder)


# In[149]:

listdir(unzip_folder)


# ## Mostre o PDF com as instruções de como usar os dados

# In[151]:

IFrame('../data/ceft_2t_TODOS_2014_UNZIP/LEIAME_CORRESP_EFETIVADA_2T.pdf', 800, 400)


# ## Copie os indices

# In[165]:

campos = [
    'DATA DA GERAÇÃO', 'HORA DA GERAÇÃO', 'CÓDIGO DO PLEITO',
    'CÓDIGO DA ELEIÇÃO', 'SIGLA DA UF', 'CÓDIGO DO MUNICÍPIO',
    'NOME DO MUNICÍPIO', 'NÚMERO DA ZONA ELEITORAL', 'NÚMERO DA SEÇÃO ELEITORAL',
    'SEQUENCIAL DE CORRESPONDÊNCIA ESPERADA', 'NÚMERO DA URNA ESPERADA', 'CÓDIGO DA CARGA ESPERADA',
    'CÓDIGO DE CARGA 1 ESPERADA', 'CÓDIGO DE CARGA 2 ESPERADA', 'CÓDIGO DO FLASHCARD DE URNA ESPERADA',
    'DATA DA CARGA DA URNA ESPERADA', 'DATA DE RECEBIMENTO DA CORRESPONDÊNCIA ESPERADA', 'SEQUENCIAL DE CORRESPONDÊNCIA EFETIVADA',
    'NÚMERO DA URNA EFETIVADA', 'CÓDIGO DA CARGA EFETIVADA', 'CÓDIGO DE CARGA 1 EFETIVADA',
    'CÓDIGO DE CARGA 2 EFETIVADA', 'CÓDIGO DO FLASHCARD DE URNA EFETIVADA', 'DATA DA CARGA DA URNA EFETIVADA',
    'DATA DE RECEBIMENTO DA CORRESPONDÊNCIA EFETIVADA', 'ORIGEM DOS VOTOS', 'DIVERGÊNCIA'
]

# por conveniência, no autocomplete,
# os nomes serão padronizados
from slugify import slugify

campos = [slugify(campo, separator='_') for campo in campos]
campos[0:5]


# ## Monte a dataframe desses dados

# In[169]:

import pandas as pd


#     - [ ] Monte a dataframe de RJ
#     - [ ] Monte uma dataframe composta de todos os arquivos

# In[174]:

rj = pd.read_csv(
    '../data/ceft_2t_TODOS_2014_UNZIP/ceft_2t_RJ_27102014134253.txt',
    encoding='latin1',
    sep=';', names=campos,
    index_col=False,
)
rj.head()


# In[177]:

len(rj)


# In[182]:

rj.loc[0]


# In[ ]:



