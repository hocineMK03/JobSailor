import React,{useState} from 'react'
import Navbar from '../components/navbar'
import Herosection from '../components/herosection'
import './homepage.css'
import Maincontentsection from '../components/maincontentsection'
import Getstarted from '../components/getstarted'
import Footer from '../components/footer'
import Cookies from 'js-cookie';
const Homepage = () => {
  let weare="homepage"
  const [isauth,setIsauth]=useState(false);
  const checkifcookie=()=>{
    const myCookieValue = Cookies.get('session_id');
    if(myCookieValue){
      
      return true;
    }
    return false;
  }
  return (
    <div className='homepage'>
      <Navbar/>
      <Herosection />
      <Maincontentsection />
      <Getstarted />
      <Footer />
    </div>
  )
}

export default Homepage
