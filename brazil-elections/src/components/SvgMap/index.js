import React from 'react'
import * as d3 from 'd3-geo'


const SvgMap = ({
      width,
      height,
      map,
      projection='geoMercator',
      ...props,
    }) => {
  const projectionFunction = d3[projection]()
    .fitSize([width, height], map)

  const paths = map
    .features
    .map(d3.geoPath(projectionFunction))

  const pathProps = Object
    .entries(props)
    .filter(([k, f]) => !!k.match(/^path/))
    .map(([k, f]) => [k[4].toLowerCase() + k.slice(5), f])

  const onPathProps = Object
    .entries(props)
    .filter(([k, f]) => !!k.match(/^onPath/))
    .map(([k, f]) => ['on' + k.slice(6), f])

  const svgProps = Object
    .entries(props)
    .filter(([k, v]) => !k.match(/^(path|onPath)/))
    .reduce((acc, [k, v]) =>
      (acc[k] = v, acc)
    , {})

  return <svg
      width={width}
      height={height}
      {...svgProps}
      >
    <g>
    {map.features.map((feature, key) =>
      <path
          {...pathProps
            .map(([k, f]) => [k, f({...feature, key})])
            .reduce((acc, [k, v]) =>
              (acc[k] = v, acc)
            , {})
          }
          {...onPathProps
            .map(([k, f]) => [k, e => f({...e, ...feature, key})])
            .reduce((acc, [k, v]) =>
              (acc[k] = v, acc)
            , {})
          }
          key={key}
          d={paths[key]}
          />
    )}
    </g>
  </svg>
}


export default SvgMap
