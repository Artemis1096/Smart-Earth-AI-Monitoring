import React from 'react'
import { Feature, Navbar } from '../components'
import "./Explanation.css"
import img from "../assets/img.jpg"
const featuresData1 = [
  {
    title: 'LULC ( Land Use and Land Cover )',
    text: "Land Use and Land Cover (LULC) refers to the classification of the Earth's surface based on the physical features (land cover) and the human activities (land use) occurring on it.",
  },
  {
    title: 'Vegetation Severity',
    text: 'Vegetation Severity refers to the extent of stress , damage , or degradation in vegetation due to environmental factors such as drought , fire , disease , deforestation , or human activity.',
  },
  {
    title: 'NDVI (Normalized Difference Vegetation Index)',
    text: 'NDVI is a satellite-based index used to measure vegetation health and greenness on Earth.',
  },
  {
    title: 'Vegetation Density Class',
    text: 'Vegetation Density Class refers to the categorization of land areas based on the amount and thickness (density) of vegetation present, usually derived from satellite indices like NDVI.',
  },
];

const demoImages = [
  {
    src: img,
    title: 'LULC Map',
    desc: 'Sample LULC classification map from satellite data.'
  },
  {
    src: img,
    title: 'NDVI Analysis',
    desc: 'NDVI index showing vegetation health.'
  },
  {
    src: img,
    title: 'Vegetation Density',
    desc: 'Map depicting vegetation density classification.'
  }
];

const Explanation = () => {
  return (
    <div>
      <Navbar />
      <hr id='nh1' />
      <div>
        <div className="gpt3__features section__padding container" id="features">
          <div className='inner-container'>
            <div className="gpt3__features-heading">
              <h1 className="gradient__text">Vegetation Model Terminology</h1>
            </div>
            <div className="gpt3__features-container">
              {featuresData1.map((item, index) => (
                <Feature title={item.title} text={item.text} key={item.title + index} />
              ))}
            </div>
          </div>
          <hr />
          <div>
            <div className="gpt3__features-heading">
              <h1 className="gradient__text demo-heading">Terminology Explanation using Images</h1>
            </div>
            <div className="demo__cards">
              {demoImages.map((image, index) => (
                <div className="demo__card" key={index}>
                  <img src={image.src} alt={image.title} className="demo__image" />
                  <h3>{image.title}</h3>
                  <p>{image.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Explanation
