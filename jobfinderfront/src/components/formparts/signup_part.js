import React from 'react'

const Signup_part = ({formdata,setFormdata}) => {
    
  return (
    <div>
      <input type='text' placeholder='name' name='name' value={formdata.name} onChange={(event)=>{
        setFormdata({...formdata,name:event.target.value} )
      }} ></input>
      <input type='text' placeholder='username' name='username' value={formdata.username} onChange={(event)=>{
        setFormdata({...formdata,username:event.target.value})
      }} ></input>
      <input type='email' placeholder='email' name='email' value={formdata.email} onChange={(event)=>{
        setFormdata({...formdata,email:event.target.value})
      }} ></input>
      <input type='password' placeholder='password' name='password' value={formdata.password} onChange={(event)=>{
        setFormdata({...formdata,password:event.target.value})
      }} ></input>
      <div className='worker'>
      <label>worker</label>
      <input type='checkbox' placeholder='isworker' name='isworker' checked={formdata.worker} onChange={(event)=>{
        setFormdata({...formdata,worker: event.target.checked})
        console.log(event.target.checked)
      }} ></input>
      </div>
    </div>
  )
}

export default Signup_part
