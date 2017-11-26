import React from 'react'
import PropTypes from 'prop-types'
import SvgMap from '../SvgMap'
import loadMaps from '../../services/brazilMaps'


const URL = '/data/all_maps.json'


export default class BrazilMap extends React.Component {
  static propTypes = {
    width      : PropTypes.number.isRequired,
    height     : PropTypes.number.isRequired,
    year       : PropTypes.number.isRequired,
    projection : PropTypes.string,
  }

  static defaultProps = {
    projection: 'geoMercator',
  }

  state = {
    maps : null,
    map  : null,
  }

  componentDidMount = () =>
    loadMaps(URL)
      .then(maps => this.setState({maps}))

  setYear = year =>
    this.setState({map: this.maps.year(year)})

  render = () => {
    const {year, ...props} = this.props

    return (!this.state.maps)
      ? <div
          className={'BrazilMap'}
          style={{
            width: this.props.width,
            height: this.props.height,
            display: 'block',
          }}
          >
        Carregando mapas...
      </div>
      : <SvgMap
          className={'BrazilMap'}
          map={this.state.maps.year(year)}
          {...props}
          />
  }
}
