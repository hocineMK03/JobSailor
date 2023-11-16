import React,{useState,useEffect} from 'react'
import './secondarynavbar.css'
import axios from 'axios';
import Cookies from 'js-cookie';
import '../herosection.css'
import Renderedmaincontent from './renderedmaincontent';
import Renderedrequestscontent from './renderedrequestscontent';
import { useNavigate } from 'react-router-dom';
const BodyBrowse = () => {
  const navigate = useNavigate();
  const handleLoginClick = () => {
    // Redirect to the login page when the button is clicked
    window.location.href = '/ResumeBuilder';
  };
  const [jobs, setJobs] = useState([]); // Initialize jobs as an empty array
  const [items, setItems] = useState([]); // Initialize items as an empty array
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [csrfToken, setCsrfToken] = useState('');
  const [itemStates, setItemStates] = useState([]); // Initialize as an array of objects with index and value
  const [isclicked,setIsclicked]=useState(false);
  const [userinfo,setUserinfo]=useState([]);
  const [pendings, setPendings] = useState([]);
  const [ifvalid,setIfvalid]=useState(false)


  
  const [showMainContent, setShowMainContent] = useState(true);
  const [whichtype,setWhichtype]=useState(1)
  let tmpbool=false
  let Job_id=0;
  let whichone=1;
  let thsiobj={}
  // Function to fetch the CSRF token
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

  const loadJobListings = (page) => {
    const session_id = Cookies.get('session_id');
    axios
      .get('http://127.0.0.1:8000/api/render/paginatejob', {
        params: { page,session_id },
        headers: {
          'X-CSRFToken': csrfToken,
        },
      })
      .then((response) => {
        const jobListings = response.data;
        const dataItems = jobListings.items;
        console.log('Items:', dataItems);
        setItems(dataItems);
        setJobs(jobListings);
        setTotalPages(jobListings.pages)
        const initialItemStates = dataItems.map(() => ({ applied: false }));
        setItemStates(initialItemStates);
        
      })
      .catch((error) => {
        console.error('Failed to fetch job listings:', error);
      });
  };
  
  const sendrequesttoapply = (tmpbool1, Job_id) => {
    // Create a JSON object with the data
    const requestData = {
      applied: tmpbool1,
      Job_id: Job_id,
    };
  
    axios
      .post('http://127.0.0.1:8000/api/joblisting/addordeletepending', requestData, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json', // Set the content type to JSON
        },
        withCredentials: true,
      })
      .then((response) => {
        const jobListings = response.data;
        // Handle the response as needed
      })
      .catch((error) => {
        console.error('Failed to send the apply request:', error);
      });
  };
  
  
  useEffect(() => {
    // Load job listings when the component mounts
    loadJobListings(currentPage);
  }, [csrfToken, currentPage]);
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
          setIfvalid(true)
          setUserinfo(response.data)
          
        }
        else{
          setIfvalid(false)
          
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


  const handleRemove = (jobId,calltype) => {
    
    axios
      .post(
        'http://127.0.0.1:8000/api/joblisting/deletependingandaccepts',
        { Job_id: jobId,
          calltype:calltype, 
        
        },
        {
          headers: {
            'X-CSRFToken': csrfToken, // Assuming csrfToken is available
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        }
      )
      .then((response) => {
        // Handle the response as needed
        console.log('Job removed successfully:', response.data);
        // Optionally, you can update the state to reflect the removal
        // For example, reload the list of pending jobs
        displaycompsbar(calltype)
            })
      .catch((error) => {
        console.error('Failed to remove job:', error);
      });
  };


  const checkifcookie=()=>{
    const myCookieValue = Cookies.get('session_id');
    if(myCookieValue){
      
      return true;
    }
    return false;
  }


  const getpendingsandrequests = (type) => {
    const session_id1 = Cookies.get('session_id');
    console.log("session id pending", session_id1);
  
    // Define the query parameters as an object
    const queryParams = {
      type: type,
      session_id: session_id1,
    };
  
    axios
      .get('http://127.0.0.1:8000/api/render/paginatepending', {
        params: queryParams,  
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json', // Set the content type to JSON
        },
        withCredentials: true,
      })
      .then((response) => {
        const pendingsandrequests = response.data;
        const pendingitems = pendingsandrequests.items;
        thsiobj=pendingitems
        console.log("thsiobj",thsiobj)
        
        setPendings(pendingitems)
        // Handle the response as needed
      })
      .catch((error) => {
        console.error('Failed to send the apply request:', error);
      });
  };
  

  
  const toggleOffered = (itemIndex) => {
    if(checkifcookie() && ifvalid){
      
      const newStates = [...itemStates]; // Copy the array of item states
      newStates[itemIndex].applied = !newStates[itemIndex].applied;
      setItemStates(newStates); // Update the item states array

      tmpbool=newStates[itemIndex].applied
      Job_id=items[itemIndex].id
      console.log(tmpbool,Job_id)
      //if yes then send a request
      sendrequesttoapply(tmpbool,Job_id)
      setDisplaycontent(
        <Renderedmaincontent items={items} itemStates={newStates} toggleOffered={toggleOffered} />
      );
    }
    else{
      navigate('/Login');
    }
  
   
  };

  
  const [displaycontent,setDisplaycontent]=useState(<Renderedmaincontent items={items} itemStates={itemStates} toggleOffered={toggleOffered} />)

  const displaycompsbar = async (whichone) => {
    console.log(whichone, "which");
    
    if (whichone === 1) {
      setShowMainContent((prevShowMainContent) => 1);
    } else {
      try {
        if (whichone === 2) {
          setWhichtype((prevShowMainContent) => 1)
          await getpendingsandrequests(1);
        } else if (whichone === 3) {
          setWhichtype((prevShowMainContent) => 2)

          await getpendingsandrequests(2);
        }
       
        setShowMainContent((prevShowMainContent) => 2);
        console.log("pending 1", pendings);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    }
    if(userinfo && whichone===5 || !userinfo && whichone===4){
      console.log("go to main profil here");

    }

    
  };
  

  const redirectfunction=(job_id)=>{
    console.log("hji",job_id)
  }
    const changenext = () => {
      if (currentPage < totalPages) {
        const nextPage = currentPage + 1;
        console.log(nextPage)
        setCurrentPage(nextPage);
        loadJobListings(nextPage);
      }
    };
    
    const changeprevious = () => {
      if (currentPage > 1) {
        const previousPage = currentPage - 1;
        console.log(previousPage)
        setCurrentPage(previousPage);
        loadJobListings(previousPage);
      }
    };
  return (
    <div className='body--container'>
      
      <div className='left'>
      <div className='left--wrapper'>
      {userinfo.type ? (
  // Condition when user.type is true 
  <ul>
    <li onClick={() => displaycompsbar(1)}>Main</li>
    <li onClick={() => displaycompsbar(2)}>Check Pendings</li>
    <li onClick={() => displaycompsbar(3)}>Check Accepts</li>
    <li onClick={handleLoginClick}><a href='/ResumeBuilder'>Customise resume</a></li>
    <li onClick={() => displaycompsbar(5)}><a href=''>Profil</a></li>
    <li onClick={() => displaycompsbar(6)}><a href=''>Customise Profil</a></li>
  </ul>
) : userinfo.type === false ? (
  // Condition when user.type is  false
  <ul>
    <li onClick={() => displaycompsbar(1)}><a href=''>Main</a></li>
    <li onClick={() => displaycompsbar(2)}><a href=''>Manage requests</a></li>
    <li onClick={() => displaycompsbar(3)}><a href=''>Check Accepts</a></li>
    <li onClick={() => displaycompsbar(4)}><a href=''>Profil</a></li>
    <li onClick={() => displaycompsbar(5)}><a href=''>Customise Profil</a></li>
  </ul>
) : (
  null
)}

      <ul>
        <li><a href='#'>Saved Searches</a></li>
        <li><a href='#'>Search Filters</a></li>
        <li><a href='#'>Job Categories</a></li>
        <li onClick={handleLoginClick}><a href='/ResumeBuilder'>Customise resume</a></li>
        <li><a href='#'>Settings and preferences</a></li>
        <li><a href='#'>Help and Support</a></li>
        <li><a href='#'>More about us</a></li>
        
      </ul>
      </div>
      
      </div>
      <div className='middle'>
    
      {userinfo.type===false ? (
  // Condition when user.type is truthy (not false or empty)
  <div className='middle--posting'>
      
      <div className='middle--body' >
      <h1> make your offer</h1>
      <input type='text' name='name' placeholder='name' />
      <input type='text' name='description' placeholder='description' />
      <input type='number' name='salary' placeholder='salary' />
      <button onClick={()=>{
        if(isclicked){
          console.log("true")
          setIsclicked(!isclicked)
        }
        else{
          console.log("false")
          setIsclicked(!isclicked)
          //set the form to appear
        }
      }}>click</button>
      
        </div>
    </div>
) : (
  // Condition when user.type is an empty string or other falsy value
  null
)}
    
 {showMainContent === 1 ? (
        <Renderedmaincontent items={items} itemStates={itemStates} toggleOffered={toggleOffered} redirectfunction={redirectfunction}/>
      ) : showMainContent === 2 ? (
        <Renderedrequestscontent pendings={pendings} whichtype={whichtype} handleRemove={handleRemove} />
      ) : (
        // Add more conditions as needed
        <Renderedmaincontent items={items} itemStates={itemStates} toggleOffered={toggleOffered} redirectfunction={redirectfunction}/>
      )}
      <div className='button-chose'>
        <button className='hero--buttons--primary' onClick={changeprevious}>previous</button>
        <button className='hero--buttons--secondary' onClick={changenext}>next</button>
      </div>
    
      </div>
      <div className='right'>
        <p>messaging features not aviable yet</p>
      </div>
    </div>
  )
}

export default BodyBrowse
