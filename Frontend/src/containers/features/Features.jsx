import React from 'react';
import Feature from '../../components/feature/Feature';
import './features.css';

const featuresData = [
  {
    title: 'Environmental Change Detection',
    text: 'Uses satellite imagery and AI to monitor deforestation, urban sprawl, and land degradation in real time.',
  },
  {
    title: 'Precision Agriculture Support',
    text: 'Monitors crop health, soil conditions, and irrigation patterns to help farmers optimize yields sustainably.',
  },
  {
    title: 'Land Use & Land Cover Classification',
    text: 'Automatically categorizes terrain types — forest, water, urban, etc. — to assess ecosystem changes over time.',
  },
  {
    title: 'Geospatial Intelligence',
    text: 'Combines spatial data with AI to generate insights for agriculture, urban planning, and biodiversity conservation.',
  },
];

const Features = () => (
  <div className="gpt3__features section__padding" id="features">
    <div className="gpt3__features-heading">
      <h1 className="gradient__text">The future is here — all you have to do is embrace it. Step into tomorrow, today, and make it your reality.</h1>
    </div>
    <div className="gpt3__features-container">
      {featuresData.map((item, index) => (
        <Feature title={item.title} text={item.text} key={item.title + index} />
      ))}
    </div>
  </div>
);

export default Features;
