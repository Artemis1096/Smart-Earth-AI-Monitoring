import React from 'react';
import './header.css';
import EarthScene from '../../components/3d Model/EarthScene';

const Header = () => (
  <div className="gpt3__header section__padding" id="home">
    <div className="gpt3__header-content">
      <h1 className="gradient__text">Smart Earth AI Monitoring</h1>
      <p>Leveraging AI-Powered Monitoring to Create a Smarter Planet, Delivering Real-Time Insights for Informed Decisions, and Paving the Way for a Sustainable Future.</p>
    </div>

    <div className="gpt3__header-image">
      {/* <img src={ai} /> */}
      <EarthScene className="earth-scene"/>
    </div>
  </div>
);

export default Header;
