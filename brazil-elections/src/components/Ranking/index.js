import React from 'react'
import Candidato from '../Candidato'
import './Ranking.css'


const Ranking = ({
      estado,
      candidatos,
      ...props,      
    }) =>
  <div
      className="Ranking"
      {...props}
      >
    <h2 className="estado">
    {
      estado
    }
    </h2>
    <div className="candidatos">
    {
      candidatos.map((el, key) => Candidato({...el, key}))
    }
    </div>
  </div>


export default Ranking
