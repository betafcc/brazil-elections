
# coding: utf-8

# In[1]:

import requests
from bs4 import BeautifulSoup as BS 

import sys
sys.path.append('..')

from src.utils import postals


# In[2]:

url_parent = 'http://www.tse.jus.br/eleicoes/eleicoes-anteriores/eleicoes-1994/resultados-das-eleicoes-1994'


# In[3]:

r = requests.get(url_parent)
soup = BS(r.text, 'html.parser')


# In[4]:

from collections import namedtuple
Resultado = namedtuple('Resultado', ['UF', 'data'])


# In[5]:

hrefs = soup.select('tr.tabelas a')
hrefs = [(list(a.strings)[0], a.attrs['href']) for a in hrefs]
hrefs = [Resultado(postals[uf], href) for uf, href in hrefs if uf != 'Brasil']


# In[6]:

print('Pegando página de resultados...')
hrefs_results = []
for uf, href in hrefs:
    r = requests.get(href)
    soup = BS(r.text, 'html.parser')
    print(uf)
    url_results = soup.find(text='Presidente').parent.attrs['href']

    hrefs_results.append(Resultado(uf, url_results))


# In[7]:

print('Pegando Tabelas...')
tables_results = []
for uf, href in hrefs_results:
    r = requests.get(href)
    soup = BS(r.text, 'html.parser')
    print(uf)
    table = soup.select('table')[0]
    
    tables_results.append(Resultado(uf, table))


# In[63]:

def structure_table(table):
    structured = []
    rows = table.data.select('tr')

    while len(rows[0].select('th')) == 0:
        del rows[0]

    header, data = rows[0], rows[1:]
    header = [
        'NUM_TURNO',
        'SIGLA_UF',
        'NOME_CANDIDATO',
        'SIGLA_PARTIDO',
        'TOTAL_VOTOS',
        'VALIDOS'
    ]

    structured.append(header)
    for dr in data:
        structured.append([1, table.UF] + [next(td.strings) for td in dr.select('td')])

    return structured


# In[64]:

tables = [structure_table(table) for table in tables_results]


# In[65]:

import pandas as pd


# In[69]:

df = pd.concat((pd.DataFrame(table[1:], columns=table[0]) for table in tables), ignore_index=True)


# In[76]:

df.NOME_CANDIDATO = df.NOME_CANDIDATO.str.slice(3)


# In[78]:

df = df.drop('VALIDOS', axis=1)


# In[ ]:

pd.to

