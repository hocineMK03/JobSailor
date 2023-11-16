import React,{useState} from 'react'
import Projects from './resumecomponents/projects';
import Contactinfo from './resumecomponents/contactinfo';
import Skills from './resumecomponents/skills';
import ReactDOMServer from 'react-dom/server';
import './resumemaker.css'; // Assuming you have a CSS file for styling

const Resumemaker = () => {
  const html2pdf = require('html2pdf.js');
  const emailRegex = /^[a-zA-Z0-9]+([_.+%-]?[a-zA-Z0-9]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  const numberRegex=/^[0-9]{10,13}$/;
  const [resumedata,setResumedata]=useState({
        name:"",
        name2:"",
        age:"",
        email:"",
        adresse:"",
        number:"",
        
  })
  const [projectdata,setProjectdata]=useState([])
  const [isvalid,setIsvalid]=useState(false)
  const[step,setStep]=useState(0);
  const[isfinished,setIsfinished]=useState(false);
  const formstepstitles=["Contact Info","Skills","Projects"];
  const pagedisplay=()=>{
      if(step==0){
          return <Contactinfo resumedata={resumedata} setResumedata={setResumedata}/>
      }
      else if(step==1){
          return <Skills />
      }
      else{
          return <Projects  />
      }
  }
  const incstep=()=>{
    
      if(step<2){
          setStep((prevShowMainContent) => prevShowMainContent+1);
         
          
      }
      if(step+1===2 && isfinished==false){
        console.log("here")
        console.log(resumedata)
        setIsfinished((prevfinished)=>!prevfinished);
        const data=[];
        
        {Object.keys(resumedata).map(key => (
          data.push([resumedata[key]])
        ))}
          console.log(data)
          checkvalid(data)
      }
      
  
      
  }

  const checkvalid = (anarray) => {
    let tmpvalid = isvalid; // Save the current state in a temporary variable
    console.log("valid", tmpvalid);
  
    if (tmpvalid === false) {
      setIsvalid((tmp) => !tmp);
      tmpvalid = true;
    }
    console.log("valid1", tmpvalid);
  
    console.log("valid2", isvalid);
  
    for (let d = 0; d < anarray.length; d++) {
      console.log(anarray[d][0]);
  
      if (anarray[d][0] === "") {
        setIsvalid((tmp) => !tmp);
        tmpvalid = false; // Set tmpvalid to false if any field is empty
        break;
      }
    }
  
    const checkemail = emailRegex.test(anarray[3][0]);
    console.log("checkk", checkemail, isvalid);
  
    if (!checkemail) {
      console.log("email non valid");
      tmpvalid = false;
    }
  
    const checknumber = numberRegex.test(anarray[5][0]);
    if (!checknumber) {
      console.log("number invalid");
      tmpvalid = false;
    }
  
    console.log("valid", tmpvalid);
  
    if (tmpvalid) {
      setIsvalid(true); // Update isvalid only if tmpvalid is true
      handlepdf();
    }
  };
  
  const decstep=()=>{
      if(step>0){
          setStep((prevShowMainContent) => prevShowMainContent-1);
         
      }
      if(step-1<2 && isfinished==true){
        setIsfinished((prevfinished)=>!prevfinished);
      }
      
  
      
  }

  const stylepage = () => {
    if (step === 0) {
        return { width: '33%' };
    } else if (step === 1) {
        return { width: '66%' };
    } else {
        return { width: '100%' };
    }
}





const handlepdf = () => {
  // Get the values from the state
  const { name, name2, age, email, adresse, number } = resumedata;

  // Create a hidden element to apply styles and values
  const contactInfoContent1 = `
    <div class="pdf--wrapper">
      <div class="pdf--header">
        <h1>Contact Info</h1>
      </div>
      <div class="pdf--body">
        <input type="text" placeholder="name" name="name" value="${name}" />
        <input type="text" placeholder="name2" name="name2" value="${name2}" />
        <input type="number" placeholder="age" name="age" value="${age}" />
        <input type="email" placeholder="email" name="email" value="${email}" />
        <input type="text" placeholder="adresse" name="adresse" value="${adresse}" />
        <input type="text" placeholder="number" name="number" value="${number}" />
      </div>
    </div>
  `;
 
  

  const contactInfoContent3 = `
  <div class="pdf--wrapper">
    <div class="pdf--header">
      <h1>Contact Info</h1>
    </div>
    <div class="pdf--body">
    <div className='form--body--parts'>
    <label>PRoject 1:</label>
    <a>google.com </a>
   </div>

   <div className='form--body--parts'>
    <label>Project 2 :</label>
    <a>google.com </a>
   </div>
   <div className='form--body--parts'>
    <label>Project 3 :</label>
    <a>google.com </a>
   </div>
    </div>
  </div>
`;

  const hiddenElement = document.createElement('div');

  // Apply styles to the hidden element
  hiddenElement.style.width = '80%';
  hiddenElement.style.margin = 'auto';
  hiddenElement.style.backgroundColor = '#f2f2f2';
  hiddenElement.style.padding = '20px';
  hiddenElement.style.borderRadius = '10px';
  hiddenElement.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';

  // Manually set the values in the rendered HTML
  // Include the entire structure, including the header
  hiddenElement.innerHTML = contactInfoContent1;
  
  hiddenElement.innerHTML += contactInfoContent3;

  // Append the hidden element to the document body
  document.body.appendChild(hiddenElement);

  // Use html2pdf to generate and save the PDF
  html2pdf().from(hiddenElement).save();

  // Remove the hidden element from the DOM
  document.body.removeChild(hiddenElement);
};







  return (
    <div className='resume'>
       
       <div className='resume--form'>
       <div className='resume--progressbar'>
        <div style={stylepage()}></div>
        </div>
        <div className='resume--container'>
        <div className='resume--header'>
        <h1>{formstepstitles[step]}</h1>
        </div>
        <div className='resume--body'>
            {pagedisplay()}
        </div>
        <div className='resume--buttons'>
            <button onClick={decstep}>previous</button>
            <button id='resumebtn' onClick={incstep}>{isfinished ? "submit" : "next"}</button>
            
        </div>
        </div>
        
       </div>

      
    </div>
    
  )
}

export default Resumemaker
