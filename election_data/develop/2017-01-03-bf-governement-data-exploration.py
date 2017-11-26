
# coding: utf-8

# # This notebook aims to:
#     - [X] Achar dados do governo sobre resultado das eleições
#     - [X] Formatar esses dados em uma dataframe
#     - [X] Aprender a transversar esses dados

# In[1]:

from IPython.display import IFrame


# In[2]:

import pandas as pd


# # Ache e mostre o site com os dados de candidatos da última eleição

# In[3]:

IFrame('http://www.tse.jus.br/hotSites/pesquisas-eleitorais/candidatos_anos/2016.html', 800, 400)


# In[ ]:




# # Faça download dos dados de candidatos da última eleição

# In[4]:

# %%bash
# wget -q -O ../data/consulta_cand_2016.zip http://agencia.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_2016.zip


# In[5]:

# %%bash
# unzip ../data/consulta_cand_2016.zip -d ../data/consulta_cand_2016 1>/dev/null


# In[6]:

get_ipython().run_cell_magic(u'bash', u'', u'ls ../data/consulta_cand_2016/')


# # Mostre o PDF com a lista de indices à amostra

# In[7]:

IFrame('../data/consulta_cand_2016/LEIAME.pdf#7', 800, 400)


# # Monte a lista de indices

# In[8]:

variaveis = [
    'DATA_GERACAO', 'HORA_GERACAO', 'ANO_ELEICAO',
    'NUM_TURNO', 'DESCRICAO_ELEICAO', 'SIGLA_UF',
    'SIGLA_UE', 'DESCRICAO_UE', 'CODIGO_CARGO',
    'DESCRICAO_CARGO', 'NOME_CANDIDATO', 'SEQUENCIAL_CANDIDATO',
    'NUMERO_CANDIDATO', 'CPF_CANDIDATO', 'NOME_URNA_CANDIDATO',
    'COD_SITUACAO_CANDIDATURA', 'DES_SITUACAO_CANDIDATURA', 'NUMERO_PARTIDO',
    'SIGLA_PARTIDO', 'NOME_PARTIDO', 'CODIGO_LEGENDA',
    'SIGLA_LEGENDA', 'COMPOSICAO_LEGENDA', 'NOME_LEGENDA',
    'CODIGO_OCUPACAO', 'DESCRICAO_OCUPACAO', 'DATA_NASCIMENTO',
    'NUM_TITULO_ELEITORAL_CANDIDATO', 'IDADE_DATA_ELEICAO', 'CODIGO_SEXO',
    'DESCRICAO_SEXO', 'COD_GRAU_INSTRUCAO', 'DESCRICAO_GRAU_INSTRUCAO',
    'CODIGO_ESTADO_CIVIL', 'DESCRICAO_ESTADO_CIVIL', 'CODIGO_COR_RACA',
    'DESCRICAO_COR_RACA', 'CODIGO_NACIONALIDADE', 'DESCRICAO_NACIONALIDADE',
    'SIGLA_UF_NASCIMENTO', 'CODIGO_MINICIPIO_NASCIMENTO', 'NOME_MUNICIPIO_NASCIMENTO',
    'DESPESA_MAX_CAMPANHA', 'COD_SIT_TOT_TURNO', 'DESC_SIT_TOT_TURNO',
    'NM_EMAIL'
]


# In[9]:

# CARAAAALHO
len(variaveis)


# # Carrege o arquivo csv como dataframe, com os indices indicados

# In[11]:

df = pd.read_csv(
    '../data/consulta_cand_2016/consulta_cand_2016_RS.txt',
    sep=';', encoding='latin1',
    index_col=False,
    names=variaveis
)


# In[12]:

df.head()


# In[13]:

df[df.NOME_CANDIDATO.str.contains('PRISCILA VOIGT')].transpose()


# # Quem ganhou as eleições de prefeito na cidade do Rio de Janeiro? 

# In[14]:

rj = pd.read_csv(
    '../data/consulta_cand_2016/consulta_cand_2016_RJ.txt',
    sep=';', encoding='latin1',
    index_col=False,
    names=variaveis
)


# In[23]:

p = rj
p = p[p.DESCRICAO_CARGO == 'PREFEITO']
p = p[p.DESC_SIT_TOT_TURNO == 'ELEITO']
p = p[p.DESCRICAO_UE == 'RIO DE JANEIRO']
p.NOME_URNA_CANDIDATO


# # Quantos vereadores foram eleitos pela cidade do Rio de Janeiro?

# In[33]:

v = rj
v = v[v.DESCRICAO_CARGO == 'VEREADOR']
v = v[v.DESCRICAO_UE == 'RIO DE JANEIRO']
g = v.groupby('DESC_SIT_TOT_TURNO')
g.size()


# # Quais os nomes dos vereadores eleitos no Rio de Janeiro?

# In[40]:

v = rj
v = v[v.DESCRICAO_CARGO == 'VEREADOR']
v = v[v.DESCRICAO_UE == 'RIO DE JANEIRO']
v = v[v.DESC_SIT_TOT_TURNO.str.startswith('ELEITO')]
v.NOME_URNA_CANDIDATO.sort_values()


# # Qual a ratio de homem/mulher nos vereadores eleitos no Rio de Janeiro?

# In[42]:

v = rj
v = v[v.DESCRICAO_CARGO == 'VEREADOR']
v = v[v.DESCRICAO_UE == 'RIO DE JANEIRO']
v = v[v.DESC_SIT_TOT_TURNO.str.startswith('ELEITO')]
g = v.groupby('DESCRICAO_SEXO')
g.size()


# In[65]:

# Porcentagem
s = g.size()
(s / (s.FEMININO + s.MASCULINO)) * 100


# # Liste todos os prefeitos eleitos no estado do RJ

# In[69]:

p = rj
p = p[p.DESCRICAO_CARGO == 'PREFEITO']
p = p[p.DESC_SIT_TOT_TURNO == 'ELEITO']
p.NOME_URNA_CANDIDATO


# In[ ]:




# # Liste quantos vereadores foram eleitos, organizados por cidade, no estado do RJ

# In[84]:

v = rj
v = v[v.DESCRICAO_CARGO == 'VEREADOR']
v = v[v.DESC_SIT_TOT_TURNO.str.startswith('ELEITO')]
v = v.groupby('DESCRICAO_UE')
v.size().sort_values(ascending=False)


# # Plote a ratio de homem/mulher vereador eleito por cidade no Rio de Janeiro

# In[153]:

v = rj
v = v[v.DESC_SIT_TOT_TURNO.str.startswith('ELEITO')]
v = v[v.DESCRICAO_CARGO == 'VEREADOR']
g = v.groupby([
    'DESCRICAO_UE',
    'DESCRICAO_SEXO'
])
s = g.size()
s


# In[154]:

u = s.unstack(1).fillna(0)
r = u.FEMININO*100 / (u.FEMININO + u.MASCULINO)
r.sort_values(ascending=False)


# In[ ]:




# In[ ]:




# In[ ]:



