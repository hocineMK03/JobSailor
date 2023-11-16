import React from 'react'

const Contactinfo = ({resumedata,setResumedata}) => {
  
 
  return (
  <>
      

<input type='text' placeholder='name' name='name' onChange={(event)=>{
 
        setResumedata({...resumedata,name:event.target.value} )
      }} ></input>
      <input type='text' placeholder='name2' name='name2'  onChange={(event)=>{
        setResumedata({...resumedata,name2:event.target.value} )
      }} ></input>
<input type='number' placeholder='age' name='age' onChange={(event)=>{
        setResumedata({...resumedata,age:event.target.value} )
      }} ></input>
<input type='email' placeholder='email' name='email' onChange={(event)=>{
        setResumedata({...resumedata,email:event.target.value} )
      }} ></input>
<input type='text' placeholder='adresse' name='adresse' onChange={(event)=>{
        setResumedata({...resumedata,adresse:event.target.value} )
      }} ></input>

<input type='text' placeholder='number' name='number'onChange={(event)=>{
        setResumedata({...resumedata,number:event.target.value} )
      }} ></input>

      
    
  </>
  )
}

export default Contactinfo
