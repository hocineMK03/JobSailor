import React, { useState,useEffect } from 'react'
import Navbar from '../components/navbar'
import SecondaryNavbar from '../components/browsecomponents/seconday navbar'
import './browse.css'
import BodyBrowse from '../components/browsecomponents/body'
import Footer from '../components/footer'
import axios from 'axios';
import Cookies from 'js-cookie';
import { useNavigate } from 'react-router-dom';
const Browse = () => {
  
    let weare="browse"
    const [isauth,setIsauth]=useState(false);
    const [csrfToken, setCsrfToken] = useState('');
    const fetchCsrfToken = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/getcsrf', {
          withCredentials: true,
        });
        const newCsrfToken = response.data.csrf_token;
        setCsrfToken(newCsrfToken);
        console.log('CSRF Token:', newCsrfToken);
      } catch (error) {
        console.error('Failed to fetch CSRF token:', error);
      }
    };
  
    useEffect(() => {
      if (!csrfToken) {
        fetchCsrfToken();
      }
    }, [csrfToken]);
    const checkvalid = () => {
      const session_id = Cookies.get('session_id');
      axios
        .get('http://127.0.0.1:8000/api/validation/validthetype', {
          params: {session_id },
          headers: {
            'X-CSRFToken': csrfToken,
          },
        })
        .then((response) => {
          
          if(response.status===200){
            setIsauth(true)
            
          }
          else{
            setIsauth(false)
            
          }
          
         
         
        })
        .catch((error) => {
          
          console.error('Failed to fetch job listings:', error);
        });
    };
    
    
    useEffect(() => {
      // Load job listings when the component mounts
      checkvalid()
    }, [csrfToken]);
  return (
    <div className='browse--page'>
      <Navbar />
      {/* <SecondaryNavbar /> */}
      <BodyBrowse />
     
    </div>
  )
}

export default Browse
