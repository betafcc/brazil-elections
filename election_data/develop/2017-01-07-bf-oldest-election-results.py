
# coding: utf-8

# # 1945 Election Results

# # This notebook aims to:
#     - [X] Achar dados do resultado da eleição de 1945
#     - [X] Baixa-los
#     - [X] Parsea-los como DataFrame
#     - [X] Aprender a traversar
#     - [X] Achar o resultado geral
#     - [X] Achar o resultado por UF

# In[3]:

from IPython.display import IFrame


# In[6]:

IFrame(
    'http://www.tse.jus.br/hotSites/pesquisas-eleitorais/resultados_anos/1945.html',
    800, 400
)


# ## Faça download dos dados

# In[7]:

from os import mkdir, listdir


# In[8]:

import wget


# In[9]:

zip_folder   = '../data/votacao_candidato_uf_1945_ZIP'
unzip_folder = '../data/votacao_candidato_uf_1945_UNZIP'


# In[12]:

# mkdir(zip_folder)
# wget.download(
#     'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_candidato_uf/votacao_candidato_uf_1945.zip',
#     out=zip_folder
# )


# In[13]:

listdir(zip_folder)


# ## Unzipe

# In[17]:

# from zipfile import ZipFile


# In[18]:

# for file in listdir(zip_folder):
#     with ZipFile(f'{zip_folder}/{file}', 'r') as zip_file:
#         zip_file.extractall(unzip_folder)


# In[19]:

listdir(unzip_folder)


# ## Mostre o PDF com instruções para o uso

# In[21]:

IFrame(
    '../data/votacao_candidato_uf_1945_UNZIP/VOTACAO_CANDIDATO_UF_1945/Leia-me.pdf#6',
    800, 600
)


# ## Copie o indice

# In[22]:

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


# ## Carregue a DataFrame dos dados do RJ

# In[23]:

import pandas as pd


# In[24]:

df = pd.read_csv(
    '../data/votacao_candidato_uf_1945_UNZIP/VOTACAO_CANDIDATO_UF_1945/VOTACAO_CANDIDATO_UF_1945_RJ.txt',
    encoding='latin1', sep=';', names=variaveis,
    index_col=False
)

df.head()


# In[25]:

len(df)


# In[26]:

df.loc[0]


# ## Quem ganhou as eleições pelo RJ?

# In[42]:

f = df[df.NUM_TURNO == 1]
f = f[f.DESCRICAO_CARGO == 'PRESIDENTE']
g = f.groupby('NOME_URNA_CANDIDATO')


# In[43]:

g.TOTAL_VOTOS.sum().sort_values(ascending=False)


# ## Carregue todos os arquivos numa única DataFrame

# In[46]:

import os
import glob


# In[49]:

path = r'../data/votacao_candidato_uf_1945_UNZIP/VOTACAO_CANDIDATO_UF_1945/'
all_files = glob.glob(os.path.join(path, '*.txt'))


# In[51]:

options = {
    'encoding': 'latin1',
    'sep': ';',
    'names': variaveis,
    'index_col': False
}

df_from_each_file = (pd.read_csv(f, **options) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)


# In[52]:

concatenated_df.head()


# In[53]:

len(concatenated_df)


# In[54]:

concatenated_df.head(1).transpose()


# ## Quem ganhou as eleições?

# In[58]:

f = concatenated_df
f = f[f.NUM_TURNO == 1]
f = f[f.DESCRICAO_CARGO == 'PRESIDENTE']


# In[59]:

g = f.groupby('NOME_URNA_CANDIDATO')


# In[64]:

s = g.TOTAL_VOTOS.sum()
s = s.sort_values(ascending=False)
s


# In[65]:

total = s.sum()
s * 100 / total


# In[ ]:




# ## Quem ganhou as eleições por estado?

# In[66]:

g = f.groupby(['SIGLA_UF', 'NOME_URNA_CANDIDATO'])


# In[70]:

by_state = g.TOTAL_VOTOS.sum()


# In[71]:

u = by_state.unstack('SIGLA_UF')


# In[72]:

u.idxmax()


# In[ ]:



