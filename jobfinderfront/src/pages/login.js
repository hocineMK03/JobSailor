import React, { useState, useEffect } from 'react';
import Login_part from '../components/formparts/loginpart';
import axios from 'axios';
import Cookies from 'js-cookie';
import './login.css'
import { useNavigate } from 'react-router-dom';
const Login = () => {
  // const history = useHistory();
  const navigate = useNavigate();
  const [formdata, setFormdata] = useState({
    name: '',
    password: '',
  });
  const [csrfToken, setCsrfToken] = useState('');
  const [message, setMessage] = useState('');
  const fetchCsrfToken = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/getcsrf', {
        withCredentials: true,
      });
      const newCsrfToken = response.data.csrf_token;
      setCsrfToken(newCsrfToken);
      console.log('CSRF Token:', newCsrfToken);
      Cookies.set('csrftoken', newCsrfToken, { domain: '127.0.0.1' });

    } catch (error) {
      console.error('Failed to fetch CSRF token:', error);
    }
  };

  useEffect(() => {
    // Fetch the CSRF token only if it's not already set
    if (!csrfToken) {
      fetchCsrfToken();
    }
  }, [csrfToken]);

  const handleFormSubmit = async () => {
    console.log(formdata)
    try {
      // Ensure the CSRF token is available before submitting the form
      if (!csrfToken) {
        console.error('CSRF token not available. Form submission halted.');
        return;
      }

      // Include the CSRF token in the headers of your request
      const response = await axios.post('http://127.0.0.1:8000/api/authentification/login', formdata, {
        headers: {
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true, // Include cookies in the request
      });
      console.log("message:", response.data.message);
      
      if (response.status === 200) {
        // Redirect the user to the desired page
        navigate('/Explore');
      } else {
        // Handle other status codes or error responses here
        console.log("hi")
        setMessage(response.data.message)
      }
    } catch (error) {
      console.error('Error while submitting the form:', error);
      
    }
  };

  return (
    <div className='signup--page'>
      <Login_part formdata={formdata} setFormdata={setFormdata} handleFormSubmit={handleFormSubmit} />
      <p >{message}</p>
    </div>
  );
};

export default Login;
