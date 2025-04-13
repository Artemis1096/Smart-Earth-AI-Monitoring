import React, { useEffect, useState } from 'react';
import Navbar from "../navbar/Navbar"

function AiMap() {
  const lat = localStorage.getItem('lat');
  const lng = localStorage.getItem('lng');
  const [mapReady, setMapReady] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
    const iframeDocument = iframe.contentWindow.document;
    const unwantedDiv = iframeDocument.querySelector('.lm-Widget.lm-Panel.jupyter-widgets-disconnected.jupyter-widgets.widget-container.widget-box.widget-vbox.geemap-light');
    
    if (unwantedDiv) {
      unwantedDiv.style.display = 'none';
    }
  };
  

  return (
    <div>
      <Navbar/>
      <div className='gradient__text heading'>Selected Area Analysis</div>
      {loading && <p>Generating map, please wait...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {mapReady && (
        <iframe
          id="mapIframe"
          src="http://localhost:5000/map"
          title="Vegetation Map"
          className='GenMap'
          onLoad={onMapLoad}
        />
      )}
    </div>
  );
}

export default AiMap;
