
import { Component } from 'react';
import './App.css';

import Homepage from './pages/homepage';
import Login from './pages/login';
import Navbar from './components/navbar';
import Form from './components/form';
import Signup from './pages/signup';
import Browse from './pages/browse';
import Resumemaker from './components/resumemaker';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';




function App() {
  
  
  return (
    <div>
        <Router>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/Home" element={<Homepage />} />
        <Route path="/Login" element={<Login />} />
        <Route path="/Register" element={<Signup />} />
        <Route path="/Explore" element={<Browse />} />
        <Route path="/ResumeBuilder" element={<Resumemaker />} />
        <Route path="*" element={<div>Page Not Found</div>} />
      </Routes>
    </Router>
    

      </div>
  );
}

export default App;
