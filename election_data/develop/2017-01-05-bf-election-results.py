
# coding: utf-8

# # Election Results

# # This notebook aims to:
#     - [X] Achar dados do resultado da última eleição
#     - [X] Baixa-los
#     - [X] Parsea-los como DataFrame
#     - [X] Aprender a traversar
#     - [X] Achar o resultado geral
#     - [X] Achar o resultado por UF
#     - [X] Achar o resultado por cidade
#     - [X] Achar o resultado por zona eleitoral

# In[1]:

from IPython.display import IFrame


# ## Mostre o site com os links para os dados

# In[2]:

IFrame(
    'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/votacao/votacao_secao_eleitoral_2014.html',
    800, 400
)


# ## Faça download dos dados

# In[3]:

from os import mkdir, listdir


# In[4]:

# import wget


# In[5]:

zip_folder   = '../data/votacao_secao_eleitoral_2014_ZIP'
unzip_folder = '../data/votacao_secao_eleitoral_2014_UNZIP'


# In[6]:

# mkdir(zip_folder)
# wget.download(
#     'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2014_BR.zip',
#     out=zip_folder
# )


# In[7]:

listdir(zip_folder)


# ## Unzipe

# In[8]:

# from zipfile import ZipFile


# In[9]:

# for file in listdir(zip_folder):
#     with ZipFile(f'{zip_folder}/{file}', 'r') as zip_file:
#         zip_file.extractall(unzip_folder)


# In[10]:

listdir(unzip_folder)


# ## Mostre o PDF com as instruções para o uso

# In[11]:

IFrame(
    '../data/votacao_secao_eleitoral_2014_UNZIP/LEIAME.pdf#14',
    800, 400
)


# ## Copie o indice

# In[12]:

variaveis = [
    'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
    'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
    'SIGLA_UE', 'CODIGO_MUNICIPIO', 'NOME_MUNICIPIO',
    'NUM_ZONA', 'NUM_SECAO', 'CODIGO_CARGO',
    'DESCRICAO_CARGO', 'NUM_VOTAVEL', 'QTDE_VOTOS'
]


# ## Carregue a DataFrame dos dados

# In[13]:

import pandas as pd


# In[14]:

df = pd.read_csv(
    '../data/votacao_secao_eleitoral_2014_UNZIP/votacao_secao_2014_BR.txt',
    encoding='latin1', sep=';', names=variaveis,
    index_col=False
)

df.head()


# In[15]:

len(df)


# In[16]:

df.loc[0]


# ## Quem ganhou as eleições?

# In[17]:

f = df[df.NUM_TURNO == 2]


# In[25]:

g = f.groupby('NUM_VOTAVEL')


# In[26]:

results = g.QTDE_VOTOS.sum()


# In[27]:

results.sort_values(ascending=False)


# ## Quem ganhou as eleições pelo estado do RJ?

# In[28]:

by_state = f.groupby(['SIGLA_UF', 'NUM_VOTAVEL']).QTDE_VOTOS.sum()


# In[29]:

by_state.RJ.sort_values(ascending=False)


# ## Quem ganhou as eleições por estado?

# In[30]:

u = by_state.unstack('SIGLA_UF')


# In[31]:

u.idxmax()


# In[ ]:



