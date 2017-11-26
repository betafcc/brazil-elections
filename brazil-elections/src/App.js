import React from 'react'
import BrazilElectionMap from './components/BrazilElectionMap'
import ReactResizeDetector from 'react-resize-detector'
import {getQuery} from './lib/util'
import debounce from 'lodash.debounce'
import './App.css'


class App extends React.Component {
  state = {
    width  : document.documentElement.clientWidth,
    height : document.documentElement.clientHeight,
  }

  initialProps = (() => {
    const {ano=2014, turno=2, estado='BR'} = getQuery()

    return {
      estado,
      ano: Number.parseInt(ano),
      turno: Number.parseInt(turno),
    }
  })()

  _onResize = () => {
    const {width, height} = window.getComputedStyle(this.App)

    this.setState({
      width: Number.parseFloat(width),
      height: Number.parseFloat(height),
    })
  }

  onResize = debounce(this._onResize, 300)

  componentDidMount = () =>
    window.addEventListener('resize', this.onResize)

  componentWillUnmount = () =>
    window.removeEventListener('resize', this.onResize)

  render = () =>
    <div
        className="App"
        ref={el => this.App = el}
        >
      <BrazilElectionMap
          width={this.state.width}
          height={this.state.width < 768
              ? null
              : Math.min(this.state.height, 600)
          }
          ano={this.initialProps.ano}
          turno={this.initialProps.turno}
          estado={this.initialProps.estado}
          />
      <ReactResizeDetector
          handleWidth
          onResize={this.onResize}
          />
    </div>
}



export default App
