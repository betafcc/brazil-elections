import React from 'react'
import PropTypes from 'prop-types'
import debounce from 'lodash.debounce'
import ReactResizeDetector from 'react-resize-detector'
import './Carousel.css'


// Get node x-centers relative to first node origin
// returns one extra entry, the total width including margin
const centers = nodes =>
  nodes
    .reduce((acc, el) => {
      let {marginLeft, width, marginRight} = getComputedStyle(el);
      [marginLeft, width, marginRight] = [marginLeft, width, marginRight]
        .map(n => Number.parseFloat(n))

      const li = acc.length - 1 // last acc index
      acc[li] = acc[li] + marginLeft + (width / 2)
      acc.push(acc[li] + (width / 2) + marginRight)

      return acc
    }, [0])


export default class Carousel extends React.Component {
  static propTypes = {
    selected : PropTypes.number,
    onLeft   : PropTypes.func,
    onRight  : PropTypes.func,
  }

  static defaultProps = {
    selected: 0
  }

  state = {}

  lisNodes = []
  lisRelativeCenters = null  
  containerNode = null


  componentDidMount = () => {
    const lisRelativeCenters = centers(this.lisNodes) 
    this.setState({ulWidth: lisRelativeCenters.pop()})
    this.lisRelativeCenters = lisRelativeCenters

    this.onResize()
  }


  _onResize = () => {
    const containerCenter = 0.5 * Number.parseFloat(
      getComputedStyle(this.containerNode).width
    )

    this.setState({
      lisCenters: this.lisRelativeCenters.map(e => containerCenter - e)
    })
  }

  onResize = debounce(this._onResize, 300)

  render = () => {
    const {lisCenters} = this.state
    const translateX = lisCenters ? lisCenters[this.props.selected] : 0
    const hasLeft  = this.props.selected !== 0 ? ' active' : ''
    const hasRight =
      this.props.selected !== React.Children.count(this.props.children) - 1
      ? ' active'
      : ''

    const lis = React.Children.map(this.props.children, (el, key) =>
      <li
          ref={n => this.lisNodes[key] = n}
          key={key}
          >
        {el}
      </li>
    )

    return <div className="Carousel">
      <div
          className={"button left" + hasLeft}
          onClick={this.props.onLeft}></div>
      <div
          ref={n => this.containerNode = n}
          >
        <ul
            style={{
              width: this.state.ulWidth,
              transform: `translateX(${translateX}px)`
            }}
            >
          {lis}
        </ul>
      </div>
      <div
          className={"button right" + hasRight}
          onClick={this.props.onRight}></div>
      <ReactResizeDetector
          handleWidth
          onResize={this.onResize} />
    </div>
  }
}
