import React from 'react';
import { Footer, Possibility, Features, What, Header } from '../containers';
import { Navbar } from '../components';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Router components
import './LandingPage.css';
import './Explanation.css'

const LandingPage = () => (
  <div className="LandingPage">
    <div className="gradient__bg">
      <Navbar />
      <hr id='nh1'/>
      <Header />
    </div>
    <What />
    <Features />
    <Possibility />
    <Footer />
  </div>
);

export default LandingPage;