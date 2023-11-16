import React from 'react'

const Personalinfo_part2 = ({formdata,setFormdata}) => {
  return (
    <div>
       

        <input type='text' name='description' placeholder='description' value={formdata.description} onChange={(event)=>{
  setFormdata({...formdata,description:event.target.value} )
}}></input>
 <input type='text' name='location' placeholder='location' value={formdata.location} onChange={(event)=>{
  setFormdata({...formdata,location:event.target.value} )
}}></input>
 
    </div>
  )
}

export default Personalinfo_part2
