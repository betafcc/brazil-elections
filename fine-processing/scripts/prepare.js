const fs = require('fs');
const path = require('path');
const topojson = require('topojson');


const DATA_ROOT = path.join(__dirname, '..', 'data');
const SRC  = path.join(DATA_ROOT, 'raw', 'all_maps_topo.json');

const DEST_MAPS = path.join(DATA_ROOT, 'deliver', 'all_maps.json');
const DEST_POSTAIS = path.join(DATA_ROOT, 'deliver', 'tabela_postais.json');


const topo = require(SRC);

topo.push((() => {  // Adicionando o mapa de 1960 baseado no de 1962, apenas mudando RR para RB
  const map1960 = JSON.parse(JSON.stringify(topo.find(({year}) => year === 1962)));
  map1960.year = 1960;
  const RR = map1960.map.objects.states.geometries.find(el => el.properties.postal === 'RR');
  RR.properties.postal = 'RB';
  RR.properties.nome = 'Território do Rio Branco';

  return map1960;
})());



const fixStates = (geoDict) => {
  const ES = getState(geoDict[1991], 'ES');
  const MG = getState(geoDict[1991], 'MG');

  setStateForAllYears(geoDict, 'ES', ES);
  setStateForAllYears(geoDict, 'MG', MG);

  return geoDict;
};


const getState = (map, postal) =>
  map
    .features
    .find(el => el.properties.postal == postal);


const setStateForAllYears = (geoDict, postal, state) =>
  Object
    .keys(geoDict)
    .forEach(year =>
      (geoDict[year]
        .features
        .find(state => state.properties.postal == postal)
        .geometry = state.geometry)
    );


let geos = topo
  .map(({year, map}) => ({  // Convert TopoJSON maps to GeoJSON
    year: year === 1962 ? 1960 : year,  // 1962 map actually is from 1960
    map: topojson.feature(map, map.objects.states),
  }))
  .map(({year, map}) => {  // Sort features by postal
    map.features.sort((a, b) =>
      (a.properties.postal < b.properties.postal) ? -1 :
      (a.properties.postal > b.properties.postal) ? 1  :
      0
    );

    return {year, map};
  })
  .reduce((acc, {year, map}) =>  // Accumulate in a single dictionary <Year, GeoJSON>
    (acc[year] = map, acc)
  , {});


// ES and MG are weird in some years, this uses the 1991 version for all
geos = fixStates(geos);

const tabelaPostais = Object
  .values(geos)
  .map(e => e.features)
  .reduce((acc, n) => acc.concat(n) , [])  // flatten
  .map(e => e.properties)
  .reduce((acc, {nome, postal}) =>
    (acc[postal] = nome, acc)
  , {});

tabelaPostais['BR'] = 'Brasil';


fs.writeFileSync(
  DEST_MAPS,
  JSON.stringify(geos),
  'utf8',
);


fs.writeFileSync(
  DEST_POSTAIS,
  JSON.stringify(tabelaPostais),
  'utf8',
);
