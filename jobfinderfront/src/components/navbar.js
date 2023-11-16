import React, { useState, useEffect } from 'react';
import './navbar.css';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

const Navbar = () => {
  const navigate = useNavigate();
  const [isauth, setIsauth] = useState(false);

  const handleLoginClick = () => {
    // Redirect to the login page when the button is clicked
    window.location.href = '/Login';
  };

  const handleLogoutClick = () => {
    Cookies.remove('session_id');
    setIsauth(false);
    navigate('/');
  };

  useEffect(() => {
    // Check the cookie status when the component mounts
    const myCookieValue = Cookies.get('session_id');
    setIsauth(!!myCookieValue);
  }, []); // Empty dependency array ensures this runs only once after the initial render

  return (
    <nav className='navbar'>
      <div className='brand'>
        <span>JobSailor</span>
      </div>
      <div className='navbar--links'>
        <a id='hm' href='/Home'>
          Home
        </a>
        <a id='explr' href='/Explore'>
          Explore
        </a>
        <a id='abtus' href='/Aboutus'>
          About Us
        </a>
        <a id='sprt' href='/Support'>
          Support
        </a>
        {isauth ? (
          // Display "Logout" button when the user is authenticated
          <button onClick={handleLogoutClick}>Logout</button>
        ) : (
          // Display "Login" button when the user is not authenticated
          <button onClick={handleLoginClick}>Login</button>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
