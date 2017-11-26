import React from 'react'
import './Candidato.css'


const Candidato = ({
      nome,
      partido,
      votos,
      imgSrc,
      className,
      ...props,
    }) => 
  <div
      className={'Candidato ' + partido + (className ? ' ' + className : '')}
      {...props}
      >
    {imgSrc ? <img src={imgSrc} alt={nome}/> : null}
    <div>
      <div className="nome">{nome}</div>
      <div className="partido">{partido}</div>
      <div className="votos">{votos.toLocaleString('pt-BR')} votos</div>
    </div>
  </div>


export default Candidato
