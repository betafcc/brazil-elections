
# coding: utf-8

# # Finding historical maps

# ## This notebook aims to:
#     - [X] Find historical map files for brazil states
#     - [X] Download them
#     - [X] Find out which relates to which election

# ## Notes:
#     - The links and IFrames here are valid as of today (2017-01-10) and may not be in the future

# In[1]:

import os
import wget


# In[2]:

from IPython.display import IFrame


# ## Mostre onde encontrar mapas históricos do Brasil

# No site mapas.ibge @2017-01-10, esse link parecia promissor:

# In[3]:

IFrame(
    'http://mapas.ibge.gov.br/politico-administrativo/2012-05-31-17-03-17.html',
    800, 400
)


# Porém ao tentar baixar os arquivos, recebo "550 Failed to change directory." do servidor

# Portanto, nesse link existe um pdf promissor:

# In[4]:

IFrame(
    'http://www.ibge.gov.br/home/geociencias/geografia/default_evolucao.shtm',
    800, 400
)


# O arquivo "Evolução da divisão territorial" contém o que procuro:

# In[5]:

# wget.download(
#     'ftp://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/evolucao_da_divisao_territorial_do_brasil_1872_2010/evolucao_da_divisao_territorial_mapas.pdf',
#     '../data/'
# )


# In[6]:

os.listdir('../data')


# In[7]:

IFrame(
    '../data/evolucao_da_divisao_territorial_mapas.pdf',
    800, 400
)


# Mas como o arquivo está em PDF, é difícil de mais pra trabalhar

# Por fim, encontrei uma boa fonte: "https://earthworks.stanford.edu/"
# que contém um ótimo banco de dados e sistema de busca:

# https://earthworks.stanford.edu/?commit=Limit&q=state+brazil&range[solr_year_i][begin]=1940&range[solr_year_i][end]=2017&search_field=dummy_range#documents
# 
# Por algum motivo a IFrame não carrega corretamente, mas os arquivos de interesse são os sob os links no formato 'State Boundaries: Brasil, < ano >'

# ## Mostre a fonte final escolhida

# Do site anterior extraio os links dos arquivos:

# Preciso Fazer um novo mapa para 1956, quando GP passa a se chamar RO
# 
# Uma outra observação para o suposto mapa de 1960, corrigo para 1962, notando que o que deveria ser Rio Branco está como Roraima apesar de RR ter sido criada em 1962

# In[8]:

maps = [
    {'year': 1940, 'url': 'http://stacks.stanford.edu/file/druid:dm443sj2820/data.zip'},
    {'year': 1950, 'url': 'http://stacks.stanford.edu/file/druid:yw498rc4263/data.zip'},
    {'year': 1956, 'url': 'http://stacks.stanford.edu/file/druid:yw498rc4263/data.zip'},
    {'year': 1962, 'url': 'http://stacks.stanford.edu/file/druid:zf548hv4473/data.zip'},
    {'year': 1970, 'url': 'http://stacks.stanford.edu/file/druid:kx233jf3889/data.zip'},
    {'year': 1980, 'url': 'http://stacks.stanford.edu/file/druid:nf449db8341/data.zip'},
    {'year': 1991, 'url': 'http://stacks.stanford.edu/file/druid:ys298mq8577/data.zip'}   
]


# ## Faça download dos mapas

# In[9]:

base_folder = '../data/historical_maps'


# In[10]:

os.mkdir(base_folder)
for map in maps:
    folder = f'{base_folder}/{map["year"]}'
    os.mkdir(folder)
    r = wget.download(map['url'], folder)
    print(r)


# In[11]:

os.listdir(base_folder)


# ## Unzipe os arquivos

# In[12]:

from glob import glob


# In[13]:

from zipfile import ZipFile

for folder in glob(f'{base_folder}/*'):
    with ZipFile(f'{folder}/data.zip', 'r') as zip_file:
        zip_file.extractall(folder)


# In[14]:

glob(f'{base_folder}/*/*')


# ## Liste os anos de eleições para presidente

# In[15]:

IFrame(
    'https://pt.wikipedia.org/wiki/Lista_de_elei%C3%A7%C3%B5es_presidenciais_no_Brasil#toc',
    800, 400
)


# In[16]:

republica_velha = [
    1891, 1894, 1898, 1902, 1906,
    1910, 1914, 1918, 1919, 1922,
    1926, 1930
]

era_vargas = [
    1934
]

republica_nova = [
    1945, 1950, 1955, 1960
]

regime_militar = [
    1964, 1966, 1969, 1974, 1978
]

nova_republica = [
    1985, 1989, 1994, 1998, 2002,
    2006, 2010, 2014
]


# In[17]:

election_years_all = (
    republica_velha + era_vargas + republica_nova +
    regime_militar  + nova_republica
)


# In[18]:

len(election_years_all)


# ## Relacione qual mapa deve ser usado pra qual eleição

# Como eu só possuo os mapas à partir de 1940, só relacionarei as eleições a partir da republica nova (1945)

# Usarei o arquivo PDF citado acima '../data/evolucao_da_divisao_territorial_mapas.pdf' e terei que assumir que ele possui todas as mudanças territoriais relevantes.
# 
# Com isso, criarei ranges em que o mapa se parmenece, supostamente, inalterado
# 
# Com detalhe para 1956 que criei e 1960 que modifiquei para 1962, como observado acima na seção dos downloads

# In[19]:

years_listed = [1872, 1900, 1911, 1920, 1933, 1940, 1950, 1956, 1962, 1970, 1980, 1991, 2000, 2010]

ranges = [range(start, end) for start, end in zip(years_listed[:-1], years_listed[1:])]
ranges += [range(years_listed[-1], 2017 + 1)]


# In[20]:

ranges


# In[21]:

map_url = [{'url': map['url'], 'map_year': map['year']} for map in maps]
map_url


# In[22]:

# associe os anos de eleiçoes com o periodo:
election_period = []
for year in election_years_all:
    for year_range in ranges:
        if year in year_range:
            election_period.append({'election_year': year, 'period': year_range})


# In[23]:

election_period


# In[24]:

final_relation = []
for election in election_period:
    for map in map_url:
        if map['map_year'] in election['period']:
            final_relation.append({**map, **election})


# Essas são as relações confiáveis (assumindo as premissas já citadas):

# In[25]:

final_relation


# Mas apesar disso vou usar o último mapa (de 1991) para todas as eleições desde então, já que empiricamente eu sei que as mudanças são irrelevantes pra minha aplicação:

# In[26]:

final_relation = []
for election in election_period:
    if election['election_year'] > 1998:
        final_relation.append({**map_url[-1], **election})
    for map in map_url:
        if map['map_year'] in election['period']:
            final_relation.append({**map, **election})


# In[27]:

final_relation


# ## Exporte as relações para JSON

# In[28]:

import json


# In[29]:

relation_copy = [{**rel} for rel in final_relation]
for relation in relation_copy:
    r = relation['period']
    relation['period'] = [r.start, r.stop]


# In[30]:

with open('../data/maps_relation.json', 'w') as f:
    f.write(json.dumps(relation_copy))


# In[31]:

os.listdir('../data/')


# In[32]:

get_ipython().run_cell_magic(u'bash', u'', u'cat ../data/maps_relation.json')


# In[ ]:



