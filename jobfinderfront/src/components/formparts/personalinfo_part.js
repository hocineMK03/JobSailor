import React from 'react'

const Personalinfo_part = ({formdata,setFormdata}) => {
  return (
    <div>
    <div>
        <input type='text' name='bio' placeholder='bio' value={formdata.bio} onChange={(event)=>{
  setFormdata({...formdata,bio:event.target.value} )
}}></input>
 <input type='text' name='skills' placeholder='skills' value={formdata.skills} onChange={(event)=>{
  setFormdata({...formdata,skills:event.target.value} )
}}></input>
 <input type='text' name='location' placeholder='location' value={formdata.location} onChange={(event)=>{
  setFormdata({...formdata,location:event.target.value} )
}}></input>
      
    </div>
    </div>
  )
}

export default Personalinfo_part
