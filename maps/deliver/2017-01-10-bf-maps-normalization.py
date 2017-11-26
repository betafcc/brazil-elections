
# coding: utf-8

# # Maps normalization

# ## This notebook aims to:
#     - [X] Relacionar nomes dos estados com sigla postal, inventar uma se necessário
#     - [X] Criar um json com essa relação
#     - [X] Adicionar no arquivo dos mapas essa sigla nos devidos estados

# ## Notes:
#     - Esse notebook usa o arquivo criado por ./2017-01-10-bf-maps-conversion.ipynb 

# In[1]:

import json


# In[2]:

with open('../data/deliver_json/all.json', 'r') as file:
    maps = json.load(file)


# In[3]:

maps[0]['map']['objects']['states']['geometries'][0]['properties']


# In[4]:

nomes = []
for map in maps:
    for geometry in map['map']['objects']['states']['geometries']:
        nomes.append(geometry['properties']['nome'])


# In[5]:

set(nomes)


# In[6]:

postals = {
    'Acre' : 'AC',
    'Alagoas' : 'AL',
    'Amapá' : 'AP',
    'Amazonas' : 'AM',
    'Bahia' : 'BA',
    'Ceará' : 'CE',
    'Distrito Federal' : 'DF',
    'Espírito Santo' : 'ES',
    'Goiás' : 'GO',
    'Maranhão' : 'MA',
    'Mato Grosso' : 'MT',
    'Mato Grosso do Sul' : 'MS',
    'Minas Gerais' : 'MG',
    'Pará' : 'PA',
    'Paraíba' : 'PB',
    'Paraná' : 'PR',
    'Pernambuco' : 'PE',
    'Piauí' : 'PI',
    'Rio de Janeiro' : 'RJ',
    'Rio Grande do Norte' : 'RN',
    'Rio Grande do Sul' : 'RS',
    'Rondônia' : 'RO',
    'Roraima' : 'RR',
    'Santa Catarina' : 'SC',
    'São Paulo' : 'SP',
    'Sergipe' : 'SE',
    'Tocantins' : 'TO',


    'Brasília': 'DF',

    'Guanabara': 'GB',

    'Território De Rondônia' : 'RO',
    'Território de Rondônia': 'RO',
    'Território de Roraima': 'RR',
    'Território do Acre': 'AC',
    'Território do Amapá': 'AP',
    'Território do Guaporé': 'GP',
    'Território do Rio Branco': 'RB'
}


# In[7]:

with open('../data/deliver_json/postals.json', 'w') as file:
    json.dump(postals, file, ensure_ascii=False)


# In[8]:

cat ../data/deliver_json/postals.json


# In[9]:

for map in maps:
    for geometry in map['map']['objects']['states']['geometries']:
        nome = geometry['properties']['nome']
        geometry['properties']['postal'] = postals[nome]


# In[10]:

with open('../data/deliver_json/all_normalized.json', 'w') as file:
    json.dump(maps, file, ensure_ascii=False)


# In[11]:

ls ../data/deliver_json/

