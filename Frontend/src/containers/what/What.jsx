import React from 'react';
import Feature from '../../components/feature/Feature';
import './Feature.css';

const What = () => (
  <div className="gpt3__whatgpt3 section__margin" id="wgpt3">
    <div className="gpt3__whatgpt3-feature">
      <Feature title="What We Do" text="Smart Earth AI Monitoring(SEAM) uses satellite images and artificial intelligence to observe and analyze the Earth’s surface. It helps detect vegetation health, classify land types like forests, urban areas, and water bodies, and spot early signs of environmental issues such as deforestation or drought. This information is shown on interactive maps to support better decision-making for sustainable development." />
    </div>
    <div className="gpt3__whatgpt3-heading">
      <h1 className="gradient__text center">The possibilities are beyond your imagination</h1>
    </div>
    <div className="gpt3__whatgpt3-container">
      <Feature title="Smart City " text="Uses satellite images and artificial intelligence to observe and analyze the Earth’s surface." />
      <Feature title="Vegetation Monitoring" text="Tracking the health and density of plant life using satellite imagery and AI." />
      <Feature title="Urban Classification" text="Uses satellite imagery to categorize land areas based on urban development. It helps in monitoring city growth, infrastructure planning, and environmental management." />
    </div>
  </div>
);

export default What;
