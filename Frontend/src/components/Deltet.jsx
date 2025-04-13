import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const Aqi = () => {
  const location = useLocation();
  const { lat, lng } = location.state || {};
  
  // State to store AQI data and handle loading/error states
  const [aqiData, setAqiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch AQI data when component mounts
  useEffect(() => {
    if (!lat || !lng) {
      setError('No coordinates provided.');
      setLoading(false);
      return;
    }

    const fetchAqiData = async () => {
      try {
        const response = await fetch('http://localhost:5000/send-coordinates-aqi', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ lat, lng }),
        });

        const data = await response.json();

        if (data.status === 'success') {
          setAqiData(data);
        } else {
          setError(data.message || 'Failed to fetch AQI data.');
        }
      } catch (err) {
        setError('An error occurred while fetching AQI data.');
      } finally {
        setLoading(false);
      }
    };

    fetchAqiData();
  }, [lat, lng]); // Re-run if lat or lng changes

  // Render content
  return (
    <div className="aqi-wrapper">
      <h1 className="aqi-title">AQI Information</h1>
      <p className="aqi-coords">Latitude: {lat || 'N/A'}</p>
      <p className="aqi-coords">Longitude: {lng || 'N/A'}</p>
  
      {loading && <p className="aqi-status">Loading AQI data...</p>}
      {error && <p className="aqi-error">Error: {error}</p>}
  
      {aqiData && (
        <div className="aqi-card">
          <h2 className="aqi-location">{aqiData.city}</h2>
          <p className = "aqi-number"><strong>Your current AQI:</strong> {aqiData.aqi}</p>
  
          <h4 className="insight">Insights : </h4>
  
          <p><strong>AQI Classification:</strong> Moderate</p>
  
          <p><strong>Improvement Suggestions:</strong></p>
          <ul className="aqi-suggestions">
            <li><strong>Citizens:</strong> Reduce personal vehicle usage, use public transport, carpool, or bike to work. Avoid burning waste and use eco-friendly fuels.</li>
            <li><strong>Local Authorities:</strong> Implement emission norms for industries, increase green cover, and optimize waste management systems.</li>
          </ul>
  
          <p><strong>Cause Analysis:</strong> The moderate AQI in Kompally Municipal Office, Hyderabad, is likely due to a combination of factors, including increasing traffic congestion, industrial activities, and construction dust in the area.</p>
        </div>
      )}
    </div>
  );
  
};

export default Aqi;