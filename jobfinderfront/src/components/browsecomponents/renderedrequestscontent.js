import React from 'react';

const Renderedrequestscontent = ({ pendings, whichtype,handleRemove }) => {
  
  return (
    <div>
      {pendings.map((reqs, index) => (
        <div className='posts' key={index}>
          <div className='posts--info'>
            <a href='#'>
              <h3>Job name : {reqs.Job_name}</h3>
            </a>
            <span>{reqs.posted_at}</span>
          </div>
          <div className='posts--body'>
            {whichtype === 2 && <p>situation: accepted</p>}
            {whichtype === 1 && <p>situation: pending</p>}
          </div>
          <div className='posts--apply'>
            <button onClick={() => handleRemove(reqs.Job_id,whichtype)}>Remove</button>
            <p>by {reqs.accepted_name}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Renderedrequestscontent;
