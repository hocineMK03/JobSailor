import React, { useState } from 'react'
import Signup_part from './formparts/signup_part';
import Personalinfo_part from './formparts/personalinfo_part';
import Others_part from './formparts/otherspart';
import Personalinfo_part2 from './formparts/personalinfo_part2';
import Others_part1 from './formparts/otherparts1';

const Form = ({validdata,setValiddata,handleFormSubmit}) => {
    const [formdata,setFormdata]=useState({
        name:"",
        username:"",
        email:"",
        password:"",
        worker:false,
        bio:"",
        skills:"",
        location:"",
        description:"",

    });
    const[step,setStep]=useState(0);
    const[isfinished,setIsfinished]=useState(false);
    const formstepstitles=["Sign Up","Personal Info","Others"];
    const[valid,setValid]=useState(false);
    
    const pagedisplay=()=>{
        if(step==0){
            return <Signup_part formdata={formdata} setFormdata={setFormdata} valid={valid} setValid={setValid}/>
        }
        else if(step==1){
            
            if(formdata.worker){
                return <Personalinfo_part formdata={formdata} setFormdata={setFormdata}/>;
            }
            else{
                return <Personalinfo_part2 formdata={formdata} setFormdata={setFormdata}/>;
            }
            
        }
        else{
            
            
            if(formdata.worker){
                return <Others_part/>;
            }
            else{
                return <Others_part1 />
            }
            
        }
    }
    const incstep =()=>{
        // check if everything is valid
        
        if(step<2){
            setStep((prevShowMainContent) => prevShowMainContent+1);
            
        }
        if(step+1===2 && isfinished==false){
            
            
             

              const data=[]
              console.log(data)
              setIsfinished((prevfinished)=>!prevfinished);
              {Object.keys(formdata).map(key => (
                
                data.push([formdata[key]])
              ))}
              if(data[4][0]==true && data[8][0]===""){
               setValid(false)
            }
            for(let d=0;d<data.length;d++){
                console.log(data[d][0])
                setValid(true)
               if(data[d][0]==='' && (d!=8)  ){

                if ((data[5][0] ==="" && data[6][0] ==="") && ( data[7][0] !="" && data[8][0] !="") ){
                    setValid(true) 
                    console.log("yesyesyes")
                }
                else if((data[8][0] ==="") && ( data[7][0] !="" && data[8][0] !="" && data[6][0] !="") ){
                    setValid(true) 
                    console.log("yesyesyes")
                }
                else{
                    console.log("not valid in ",d,data[d][0])
                    setValid(false)
                    
                    break;
                }
                   
                
                
               }
               
            }
            console.log("isvalid",valid)
            if(valid){
                
                setValiddata({
                    name: formdata.name,
                    username: formdata.username,
                    email: formdata.email,
                    password: formdata.password,
                    worker: formdata.worker,
                    bio:formdata.bio,
                    skills:formdata.skills,
                    location:formdata.location,
                    description:formdata.description,
                  });
                  
                console.log("isvalid",formdata)
                console.log("isvalid2",validdata)
                setIsfinished((tmp)=>true)
            }
            else{
                setIsfinished((tmp)=>false)
                console.log("is not valid")
            }
          }
       
                
                
        
    }
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
    };
    
  return (
    <div className='form'>
       <div className='form--image'>

       </div>
       <div className='form--form'>
       <div className='progressbar'>
        <div style={stylepage()}></div>
        </div>
        <div className='form--container'>
        <div className='form--header'>
        <h1>{formstepstitles[step]}</h1>
        </div>
        <div className='form--body'>
            {pagedisplay()}
        </div>
        <div className='form--buttons'>
            <button onClick={decstep}>previous</button>
            {valid && isfinished ? (
          // Display "Logout" button when the user is authenticated
          <button onClick={handleFormSubmit}>Submit</button>
        ) : (
          // Display "Login" button when the user is not authenticated
          <button id='btnsubmit' onClick={incstep}>Next</button>
            
        )}
        </div>
        </div>
        
       </div>

      
    </div>
  )
}

export default Form


// if valid then send a call to backend