import React from 'react'

const Renderedmaincontent = ({ items, itemStates, toggleOffered,redirectfunction }) => {
 
  return (
        <div>
          {items.map((item, index) => (
            <div className='posts' key={index} onClick={()=>redirectfunction(items[index].id)}>
              
              <div className='posts--info' >
                <a href='' ><h3 >{item.posted_by}</h3></a>
                <span>{item.posted_at}</span>
              </div>
              <div className='posts--body'>
                <h2><a href=''>{item.name}</a>, <a href=''>{item.category}</a></h2>
                <p>{item.description}</p>
                <span>starting at 10000  d.a</span>
              </div>
              <div className='posts--apply'>
                <button
                  onClick={() => toggleOffered(index)}
                  className={itemStates[index].applied ? 'offered-button' : 'not-offered-button'}
                >
                  {itemStates[index].applied ? 'cancel' : 'apply'}
                </button>
                <span >number of appliers</span>
              </div>
            </div>
          ))}



        </div>
  )
}

export default Renderedmaincontent
