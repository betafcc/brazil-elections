
# coding: utf-8

# # General TSE election data loader

# ## This notebook aims to:
#     - [ ] Copiar todas as tabelas de colunas de dados
#     - [ ] Fazer um dicionario e um JSON disso
#     - [ ] Fazer uma função que identifica qual tabela usar
#     - [ ] Fazer um loader que identifica automaticamente as configurações a partir da estrutura do nome do arquivo

# In[1]:

from IPython.display import IFrame


# ## Faça download das instruções de arquivos mais recentes

# In[6]:

import wget
import os

folder = '../data/loader'
os.mkdir(folder)
wget.download(
    'http://agencia.tse.jus.br/estatistica/sead/eleicoes/eleicoes2016/correspefet/ceft_2t_AL_01112016175139.zip',
    folder
)


# In[7]:

os.listdir(folder)


# ## Unzipe

# In[8]:

from zipfile import ZipFile

with ZipFile('../data/loader/ceft_2t_AL_01112016175139.zip', 'r') as zip:
    zip.extractall('../data/loader/')


# In[9]:

os.listdir(folder)


# In[ ]:




# In[ ]:




# In[2]:

IFrame(
    '../data/results_ALL/unzipped/2014/LEIAME.pdf',
    800, 400
)


# In[ ]:

options = {
    'encoding': 'latin1',
    'sep': ';',
    'names': get_columns_names(year),
    'index_col': False
}


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



