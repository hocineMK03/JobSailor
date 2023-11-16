import React from 'react'
import './maincontentsection.css'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import  {faHandshakeAngle,faThumbsUp,faFaceSmile} from '@fortawesome/free-solid-svg-icons'
const Maincontentsection = () => {
  return (
    
      <div className='maincontent--cards'>
        <div className='maincontent--card'>
          <FontAwesomeIcon icon={faHandshakeAngle} className='icn'></FontAwesomeIcon>
        <h2>App Features</h2>
        <p>Discover a  range of features that simplify your job search including filters,built in messaging system and bookmarks</p>

        </div>


        <div className='maincontent--card'>
        <FontAwesomeIcon icon={faThumbsUp} className='icn'></FontAwesomeIcon>
        
        <h2>how it Works</h2>
            <p>Sign up and create your profile,search for job apllication and then wait for a responce</p>

        </div>


        <div className='maincontent--card'>
        <FontAwesomeIcon icon={faFaceSmile} className='icn'></FontAwesomeIcon>
        
        <h2>Employer Benefits</h2>
            <p>we understand that employers also have unique needs when it comes to finding the right candidates,so we included a built it resume viewer</p>
           
        </div>
      </div>
  
  )
}

export default Maincontentsection
