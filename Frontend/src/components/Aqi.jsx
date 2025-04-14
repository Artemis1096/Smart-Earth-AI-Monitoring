import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import NavBar from "./navbar/Navbar"
import { useNavigate } from 'react-router-dom';
import "./Aqi.css"
const Aqi = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { lat, lng } = location.state || {};

  // State to store AQI data and handle loading/error states
  const [aqiData, setAqiData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to determine the AQI classification and color
  const getAqiClassification = (aqi) => {
    if (aqi <= 50) {
      return { classification: 'Good', color: '#28a745' }; // Green
    } else if (aqi <= 100) {
      return { classification: 'Moderate', color: '#ffc107' }; // Yellow
    } else if (aqi <= 150) {
      return { classification: 'Unhealthy', color: '#fd7e14' }; // Orange
    } else if (aqi <= 200) {
      return { classification: 'Very Unhealthy', color: '#dc3545' }; // Red
    } else {
      return { classification: 'Hazardous', color: '#6f42c1' }; // Purple
    }
  };

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
          setAqiData(data);  // Assuming 'insight' comes as HTML in the response
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
    <div>
      <NavBar/>
    <div className="aqi-wrapper">
      <h1 className="gradient__text">AQI Information</h1>
      <br />
      <p className="aqi-coords">Latitude: {lat || 'N/A'}</p>
      <p className="aqi-coords">Longitude: {lng || 'N/A'}</p>
      <br />

      {loading && <p className="gradient__text">Loading AQI and AI generating ...</p>}
      {error && <p className="aqi-error">Error: {error}</p>}
      
      {aqiData && (
        <div className="aqi-card">
          <h2 className="gradient__text">
            {aqiData.city}
          </h2>
          <br />
          <p className="aqi-number">
            <strong className='gradient__text'>AQI:</strong> {aqiData.aqi}
          </p>
          <h3 className="insight">Insights:</h3>
          <br />
          <div
            className="aqi-insights"
            dangerouslySetInnerHTML={{ __html: aqiData.insight }}  // Render HTML from AI
          />
        </div>
      )}
    </div>

    <button className='btn' onClick={() => navigate('/report')}>getReport</button>
    
    </div>
  );
};

export default Aqi;
