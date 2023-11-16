import React from 'react'

const Login_part = ({formdata,setFormdata,handleFormSubmit }) => {
    
  const stylepage = () => {
    return { width: '0%' };
  }
  return (
   



<div className='form'>
       <div className='form--image'>

       </div>
       <div className='form--form'>
       
        <div className='form--container'>
        <div className='form--header'>
        <h1>Login</h1>
        </div>
        <div className='form--body'>
        <input type='text' placeholder='name' name='name' value={formdata.name} onChange={(event)=>{
        setFormdata({...formdata,name:event.target.value} )
      }} ></input>
      <input type='password' placeholder='password' name='password' value={formdata.password} onChange={(event)=>{
        setFormdata({...formdata,password:event.target.value})
      }} ></input>
        </div>
        <div className='form--buttons'>
        <button onClick={handleFormSubmit }>Login</button>
        </div>
        </div>
         {/* <a href='#'>forgot password</a>
        <a href='#'>create a new account</a> */}
       </div>

      
    </div>
  )
}

export default Login_part
