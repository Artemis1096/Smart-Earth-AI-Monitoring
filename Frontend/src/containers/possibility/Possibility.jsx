import React from 'react';
import possibilityImage from '../../assets/img.jpg';
import './possibility.css';

const Possibility = () => (
  <div className="gpt3__possibility section__padding" id="possibility">
    <div className="gpt3__possibility-image">
      <img src={possibilityImage} alt="possibility" />
    </div>
    <div className="gpt3__possibility-content">
      <h1 className="gradient__text">The potential is limitless when innovation leads the way.</h1>
      <p>By combining satellite imagery with AI, we enable real-time monitoring of vegetation, and urban areas — empowering smarter decisions and unlocking endless possibilities for a sustainable future.</p>
    </div>
  </div>
);

export default Possibility;
