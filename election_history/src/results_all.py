from .results_1945_1989 import resultados_turnos as r_1945_1989
from .results_1994_2014 import resultados_turnos as r_1994_2014
from .results_1994 import resultados_turnos as r_1994
from .results_1998 import resultados_turnos as r_1998
from .results_2002 import resultados_turnos as r_2002 
from .results_2006 import resultados_turnos as r_2006

from .utils import ano_turnos

import json

def resultados_turnos(ano, turnos):
    if ano in range(1945, 1989 + 1):
        return r_1945_1989(ano, turnos)
    if ano in range(1994, 2014 + 1):
        if ano == 1994:
            return r_1994(ano, turnos)
        elif ano == 1998:
            return r_1998(ano, turnos)

        return r_2002(ano, turnos)
        # elif ano == 2006:
            # return r_2006(ano, turnos)
        # else:
            # return r_1994_2014(ano, turnos)

def main():
    resultados = []
    for ano, turnos in ano_turnos:
        resultados.extend(resultados_turnos(ano, turnos))
    return resultados

def to_json(path):
    resultados = main()
    with open(path, 'w') as file:
        json.dump(resultados, file, ensure_ascii=False)
    print('FINALLY')

    return resultados
