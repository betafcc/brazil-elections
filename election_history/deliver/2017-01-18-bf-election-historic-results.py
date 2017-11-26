
# coding: utf-8

# In[1]:

import os
import shutil
import wget
import pandas as pd
from glob import glob
from zipfile import ZipFile


# In[2]:

from sys import path
path.append('..')


# In[3]:

# os.mkdir('../data/working')
# os.mkdir('../data/clean')


# ## 1945-2014

# In[4]:

from src.results_all import to_json
r = to_json('../data/clean/elections.json')


# In[5]:

for e in r:
    print(e['ano'], len(e['estados']))


# In[6]:

# from src.results_1945_1989 import carregar


# In[7]:

# df_1955 = carregar(1955)
# df_1960 = carregar(1960)


# In[8]:

# list(zip(sorted(df_1955.SIGLA_UF.unique()), sorted(df_1960.SIGLA_UF.unique())))


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



