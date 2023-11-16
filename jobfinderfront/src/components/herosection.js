import React from 'react'
import './herosection.css'
const Herosection = () => {
  const handleLoginClick = () => {
    // Redirect to the login page when the button is clicked
    window.location.href = '/Register';
  };
  return (
    <div className='herosection--container'>

<div className='hero--container'>
      <div className='hero--left'>
      <div className='hero--text'>
      <h1>Find Your Dream Job with <span>JobSailor</span></h1>
      <div className='line'></div>
          <p>Discover, Apply, and Connect with Job Opportunities</p>
        
        </div>
          
      <div className='hero--buttons'>
      <button className='hero--buttons--primary'>Learn More</button>
        <button className='hero--buttons--secondary' onClick={handleLoginClick}>Get Started !</button>
     
        </div>
      </div>
      <div className='hero--right'>

      </div>
    </div>

    </div>
    
     
  )
}

export default  Herosection
