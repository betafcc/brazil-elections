export default async function (url) {
  const json = await (await fetch(url)).json()
  const elections = json
    .map(expandElection)
    .map(addBR)

  const election = (year, turn=1) =>
    elections.find(({ano, turno}) =>
      ano === year &&
      turno === turn
    )

  const index = (year, turn=1) =>
    elections.findIndex(({ano, turno}) =>
      ano === year &&
      turno === turn
    )

  return {
    elections,
    election,
    index,
  }
}


const expandElection = ({estados, candidatos, ...args}) =>
  ({
    candidatos,
    estados: expandAllStates(candidatos, estados),
    ...args,
  })


const expandAllStates = (tabelaCandidatos, estados) =>
  Object
    .entries(estados)
    .map(([postal, ranking]) =>
      [postal, expandState(tabelaCandidatos, ranking)]
    )
    .reduce((acc, [k, v]) =>
      (acc[k] = v, acc)
    , {})


const expandState = (tabelaCandidatos, ranking) =>
  ranking
    .map(({candidato, ...args}) => ({
      candidato: tabelaCandidatos[candidato],
      ...args,
    }))


const addBR = ({estados, candidatos, ...args}) =>
  ({
    estados: Object.assign(estados, {'BR': candidatos.map(c => ({candidato: c, votos: c.votos}))}),
    candidatos,
    ...args,
  })