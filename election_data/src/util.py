
republica_nova = [1945, 1950, 1955, 1960]
regime_militar = [1964, 1966, 1969, 1974, 1978]
nova_republica = [1985, 1989, 1994, 1998, 2002, 2006, 2010, 2014]

YEARS = republica_nova + regime_militar + nova_republica
# 1985 foi indireta por decisão judicial 
DIRETAS = republica_nova + nova_republica[1:]

base = '../data/results_ALL'
paths = {
    'base': base,
    'zip': f'{base}/zip',
    'unzip': f'{base}/unzip',
    'normalized': f'{base}/normalized',
    'json': f'{base}/json'
}
