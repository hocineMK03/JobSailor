import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import  {faMessage,faEarth,faNoteSticky,faContactCard,faSignal} from '@fortawesome/free-solid-svg-icons'
import React from 'react'
import './secondarynavbar.css'
const SecondaryNavbar = () => {
  return (
    <div className='secondnav'>
      
      
     <div className='secondnav--wrapper'>
     <a  href='/Messaging'><FontAwesomeIcon className='icn1' icon={faMessage}></FontAwesomeIcon></a>
    <a href='/Notifications'><FontAwesomeIcon className='icn1' icon={faEarth}></FontAwesomeIcon></a>
    <a href='/Notifications'><FontAwesomeIcon className='icn1' icon={faNoteSticky}></FontAwesomeIcon></a>
    <a href='/Notifications'><FontAwesomeIcon className='icn1' icon={faContactCard}></FontAwesomeIcon></a>
       
     </div>
    </div>
  )
}

export default SecondaryNavbar
