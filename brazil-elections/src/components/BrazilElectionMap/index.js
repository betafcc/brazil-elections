import React from 'react'
import PropTypes from 'prop-types';

import Swipeable from 'react-swipeable'

import Carousel from '../Carousel'
import BrazilMap from '../BrazilMap'
import Ranking from '../Ranking'

import {setQuery} from '../../lib/util'
import elections from '../../services/elections'

import './BrazilElectionMap.css'


export default class BrazilElectionMap extends React.Component {
  static propTypes = {
    width       : PropTypes.number.isRequired,
    height      : PropTypes.number,

    ano         : PropTypes.number.isRequired,
    turno       : PropTypes.number,
    estado      : PropTypes.string,
  }

  static defaultProps = {
    turno  : 1,
    estado : '',
  }

  state = {
    ano: this.props.ano,
    turno: this.props.turno,
    estado: this.props.estado,
  }


  componentDidMount = () => {
    elections('/data/elections.json')
      .then(elections => (this.setState({elections}), window.elections = elections))

    fetch('/data/tabela_postais.json')
      .then(r => r.json())
      .then(postais => this.setState({postais}))

    this.setQuery()
  }

  setQuery = () => {
    const {ano, turno, estado} = this.state
    setQuery({ano, turno, estado})
  }

  handleKeyPress = e => {
    const {key} = e

    if (key === 'ArrowLeft' || key === 'ArrowRight')
      e.preventDefault()
    if (key === 'ArrowLeft')
      this.shift(-1)
    if (key === 'ArrowRight')
      this.shift(1)
  }

  currentElection = () =>
    this.state.elections.election(this.state.ano, this.state.turno)

  findCurrentElectionIndex = () =>
    this.state.elections.index(this.state.ano, this.state.turno)

  shift = (n) => {
    // find current index
    const i = this.findCurrentElectionIndex()

    // shift cyclacly
    const {elections} = this.state.elections
    const {ano, turno} = elections[(i + n + elections.length) % elections.length]

    this.setState({ano, turno}, this.setQuery)
  }

  getCandidatos = () => {
    const {estados, candidatos} = this.currentElection()

    const estado = estados[this.state.estado]

    if (estado)
      return estado.map(({candidato, votos}) => ({...candidato, votos}))

    setTimeout(_ => this.setState({estado: 'BR'}), 0)  // HACK
    return candidatos
  }

  pathClassName = ({properties: {postal}}) => {
    let className = postal

    className += ' ' + this
      .currentElection()
      .estados[postal][0]
      .candidato
      .partido

    if (this.state.estado === 'BR' || postal === this.state.estado)
      className += ' focus'

    return className
  }

  renderTimeline = () =>
    <Carousel
        selected={this.findCurrentElectionIndex()}
        onLeft={_ => this.shift(-1)}
        onRight={_ => this.shift(1)}
        >
    {this.state.elections.elections.map(({ano, turno}, key) =>
      <a
          className={
            ((ano === this.state.ano) && (turno === this.state.turno))
            ? 'selected'
            : null
          }
          onClick={_ => this.setState({ano, turno}, this.setQuery)}
          key={key}>
        {ano + '-' + turno}
      </a>
    )}
    </Carousel>

  renderRanking = () =>
    <Ranking
        estado={this.state.postais[this.state.estado]}
        candidatos={this.getCandidatos()}
        />

  calculateSize = () => {
    const {width, height} = this.props

    if (this.props.width < 768) {
      const n = Math.min(width, 500)
      return {width: n, height: n}
    }

    const n = Math.min(this.props.height, width * 0.69)
    return {width: n, height: height - 42}
  }

  render = () =>
    <div
        ref={div => (div && div.focus) ? div.focus() : null}
        onKeyDown={this.handleKeyPress}
        tabIndex="0"
        className={'BrazilElectionMap' + ((this.props.width < 768) ? '' : ' large')}
        style={{
          boxSizing: 'border-box',
          width: this.props.width,
          height: this.props.height,
        }}
        >
      <Swipeable
          onSwipedRight={_ => this.shift(-1)}
          onSwipedLeft={_ => this.shift(1)}
          className="Main"
          >
        <BrazilMap
            style={{
              display: 'block',
              margin: '0 auto',
            }}
            {...this.calculateSize()}
            year={this.state.ano}
            pathClassName={this.pathClassName}
            onClickCapture={e => this.setState({estado: 'BR'}, this.setQuery)}
            onPathClick={e => this.setState({estado: e.properties.postal}, this.setQuery)}
            />
        {this.state.elections ? this.renderTimeline() : null}
      </Swipeable>
      {(this.state.elections && this.state.postais) ? this.renderRanking() : null}
    </div>
}
