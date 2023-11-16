import React from 'react'
import './maincontentsection.css'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import  {faMagnifyingGlass} from '@fortawesome/free-solid-svg-icons'
import './herosection.css'
const Getstarted = () => {
  return (
    <div className='started'>
      <div className='searchbar'>
        <FontAwesomeIcon icon={faMagnifyingGlass}></FontAwesomeIcon>
        <div className='blocked'>
        <p>JobSailor.com</p>
      
        </div>
      
      </div>
      <button className='hero--buttons--primary'>Get Started</button>
    </div>
  )
}

export default Getstarted
