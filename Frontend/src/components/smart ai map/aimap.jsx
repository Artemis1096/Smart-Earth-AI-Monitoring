import React, { useEffect, useState } from 'react';
import Navbar from "../navbar/Navbar";
import { useNavigate } from 'react-router-dom';

import "./SmartCity.css"
function AiMap() {
  const lat = localStorage.getItem('lat');
  const lng = localStorage.getItem('lng');
  const navigate = useNavigate();
  const [mapReady, setMapReady] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showMap2, setShowMap2] = useState(false);

  const sendCoordinates = async () => {
    try {
      const response = await fetch('http://localhost:5000/send-coordinates', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lng }),
      });
      const result = await response.json();
      if (result.status === 'success') {
        console.log('Map is ready');
        setMapReady(true);
      } else {
        setError('Map generation failed: ' + result.message);
      }
    } catch (err) {
      setError('Error while sending coordinates: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (lat && lng) {
      sendCoordinates();
    } else {
      setError('Latitude and longitude not found');
      setLoading(false);
    }
  }, [lat, lng]);

  const onMapLoad = () => {
    const iframe = document.getElementById('mapIframe');
    const iframeDocument = iframe?.contentWindow?.document;
    const unwantedDiv = iframeDocument?.querySelector(
      '.lm-Widget.lm-Panel.jupyter-widgets-disconnected.jupyter-widgets.widget-container.widget-box.widget-vbox.geemap-light'
    );
    if (unwantedDiv) {
      unwantedDiv.style.display = 'none';
    }
  };

  return (
    <div>
      <Navbar />
      <div className='gradient__text heading'>Selected Area Analysis</div>
      {loading && <p>Generating map, please wait...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {mapReady && !showMap2 && (
        <>
          <div className='map-container'>
            <iframe
              id="mapIframe"
              src="http://localhost:5000/map"
              title="Vegetation Map"
              className='GenMap'
              onLoad={onMapLoad}
            />
            <div className='info-container'>
              <h1 className='gradient__text info-heading'>Image Info</h1>
              <ul className='info-list'>
                <li>1. Blue Color is representing Water</li>
                <li>2. Purple Color is representing Roads</li>
                <li>3. Yellow Color is representing Buildings</li>
                <li>4. Black Color is representing Vacant Areas that can be used for development</li>
                <li>5. If Uncolored it is not a part of Urban Demographic</li>
                <li></li>
              </ul>
            </div>
          </div>
          <div style={{ marginTop: '20px' }}>
            <button className='btn' onClick={() => setShowMap2(true)}>Next Page</button>
          </div>
        </>
      )}

      {showMap2 && (
        <>
          <div className="map-container">
            <iframe
              id="map2Iframe"
              src="http://localhost:5000/map2"
              title="Secondary Map"
              className='GenMap'
              
            />
            <div className='info-container'>
              <h1 className='gradient__text info-heading'>Image Info</h1>
              <ul className='info-list'>
                <li>Initially all are layers are selected, you can deselect them all to get a clear picture of the map</li>
                <li>1. Grouped LULC - Grouped_LULC is a map that shows different types of land — like water, forests, cities, etc.</li>
                <li>2. Classified LULC - Classified LULC is a map that the computer made by guessing what type of land is where — based only on the vegetation (NDVI) data.</li>
                <li>3. NDVI - NDVI (Normalized Difference Vegetation Index) is a numerical indicator that uses satellite images to measure the presence and health of vegetation on Earth.</li>
                <li>4. Vegetation Density - Vegetation density tells us how much plant life is present in an area and how thick or healthy that plant life is.</li>
                <li>5. Vegetation Severity - Vegetation severity shows how badly an area is lacking healthy vegetation.</li>
              </ul>
            </div>
          </div>
          <button className='btn' onClick={() => navigate('/aqi', { state: { lat, lng } })}>
            View AQI
          </button>

        </>
      )}
      
    </div>
    
  );
}

export default AiMap;
