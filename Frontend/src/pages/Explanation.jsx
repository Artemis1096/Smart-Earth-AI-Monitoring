import React from 'react'
import { Feature, Navbar } from '../components'
import "./Explanation.css"
import img from "../assets/img.jpg"
import ClassifiedLULC from "../assets/Classified LULC.png"
import GroupedLULC from "../assets/Grouped LULC.png"
import NDVI from "../assets/NDVI.png"
import VegetationDensity from "../assets/Vegetation Density.png"
import VegetationSeverity from "../assets/Vegetation Severity.png"

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
    src: GroupedLULC,
    title: 'Grouped LULC',
    desc: 'Grouped_LC is a map that shows different types of land — like water, forests, cities, etc. Blue for Water, Orange for Vegetation, Red for Urban Areas, Gray for others ( Snow, Clouds or Unknown areas.)'
  },
  {
    src: ClassifiedLULC,
    title: 'Classified LULC',
    desc: 'Classified LULC is a map that the computer made by guessing what type of land is where — based only on the vegetation (NDVI) data.'
  },
  {
    src: NDVI,
    title: 'NDVI',
    desc: 'NDVI (Normalized Difference Vegetation Index) is a numerical indicator that uses satellite images to measure the presence and health of vegetation on Earth.'
  },
  {
    src: VegetationDensity,
    title: 'Vegetation Density',
    desc: 'Vegetation density tells us how much plant life is present in an area and how thick or healthy that plant life is.'
  },
  {
    src: VegetationSeverity,
    title: 'Vegetation Severity',
    desc: 'Vegetation severity shows how badly an area is lacking healthy vegetation.Its based on how low or high the NDVI (Normalized Difference Vegetation Index) is.'
  }
];

const Explanation = () => {
  return (
    <div>
      <Navbar />
      {/* <hr id='nh1' /> */}
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
