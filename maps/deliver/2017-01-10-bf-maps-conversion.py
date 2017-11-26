
# coding: utf-8

# # Maps coversion to TOPOJSON

# ## This notebook aims to:
#     - [X] Converter cada shapefile de mapa para seu formato topojson
#     - [X] Produzir um único JSON que contém a relação dos topojson e ano

# ## Notes:
#     - Esse notebook usa os arquivos criados em ./2017-01-10-bf-historical-maps.ipynb
#     - Esse notebook tem como dependências os binários 'ogr2ogr', 'geo2topo' e 'toposimplify'
#     - O formato do arquivo final é um JSON na estrutura:
#         [{"year": < ano >}]

# ## Converta mapas para GeoJSON

# In[1]:

get_ipython().run_cell_magic(u'bash', u'', u'infolder=../data/historical_maps\noutfolder=../data/maps_conversion\nmkdir $outfolder\nfor map_year in $(ls $infolder); do\n    mkdir $outfolder/$map_year\n    ogr2ogr -f GeoJSON -t_srs "EPSG:4326" $outfolder/$map_year/states.json $infolder/$map_year/*.shp\ndone')


# Lembrando da observação feita no notebook anterior, eu baixei o mapa de 1950 para representar 1956, já que as fronteiras são as mesmas, mas para ficar correto, tenho que corrigir o nome de Território de Guaporé para Território de Rondônia

# In[2]:

get_ipython().run_cell_magic(u'bash', u'', u"sed -i -e 's/Territ\xf3rio do Guapor\xe9/Territ\xf3rio de Rond\xf4nia/' ../data/maps_conversion/1956/states.json")


# ## Converta para TopoJSON

# In[3]:

get_ipython().run_cell_magic(u'bash', u'', u'folder=../data/maps_conversion\nfor map_year in $(ls $folder); do\n    geo2topo -o $folder/$map_year/states.topo.json -- $folder/$map_year/states.json\ndone')


# ## Simplifique os arquivos

# In[4]:

get_ipython().run_cell_magic(u'bash', u'', u'folder=../data/maps_conversion\nfor map_year in $(ls $folder); do\n    toposimplify $folder/$map_year/states.topo.json -P 0.1 -f \\\n        -o $folder/$map_year/states_simplified.topo.json\ndone')


# In[5]:

get_ipython().run_cell_magic(u'bash', u'', u'du -h ../data/maps_conversion/*/*.json')


# In[6]:

get_ipython().run_cell_magic(u'bash', u'', u'folder=../data/maps_conversion\ndest=../data/deliver_json\n\nmkdir $dest\nfor map_year in $(ls $folder); do\n    echo "{\\"year\\": $map_year, \\"map\\":" \\\n        $(cat $folder/$map_year/*simplified.topo.json) \\\n        "}" > $dest/$map_year.json\ndone')


# In[7]:

get_ipython().run_cell_magic(u'bash', u'', u'ls ../data/deliver_json/')


# In[8]:

from glob import glob
import os
import json


# In[9]:

contents = []
for file_path in glob('../data/deliver_json/*'):
    with open(file_path, 'r') as file:
        contents.append(json.load(file))


# In[10]:

contents = sorted(contents, key=lambda d: d['year'])


# In[11]:

with open('../data/deliver_json/all.json', 'w') as file:
    json.dump(contents, file, ensure_ascii=False)


# In[12]:

ls ../data/deliver_json/

