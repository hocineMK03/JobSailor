import React from 'react';
import './footer.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFacebook, faInstagram, faLinkedin } from '@fortawesome/free-brands-svg-icons';

const Footer = () => {
  return (
    <footer>
      <h1>CONTACT US</h1>
      <div className='footer--container'>
        <div className='footer--text'>
          <h2>Getting in touch is easy</h2>
          <p>Just fill out the form below:</p>
          <span>Support: hocine182003@gmail.com</span>
          <div className='footer--socialmedia'>
          <a href="https://www.facebook.com" >
  <FontAwesomeIcon icon={faFacebook} className="icn" />
</a>
<a href="https://www.facebook.com" >
  <FontAwesomeIcon icon={faInstagram} className="icn"/>
</a>
<a href="https://www.facebook.com" >
  <FontAwesomeIcon icon={faLinkedin} className="icn" />
</a>

          </div>
        </div>
        <div className='footer--form'>
          <input type='text' placeholder='Name' />
          <input type='email' placeholder='Email' />
          <textarea placeholder='Message'></textarea>
          <button type="submit">Submit</button>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
