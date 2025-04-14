import React, { useState, useEffect } from 'react';
import NavBar from "./navbar/Navbar";
import "./report.css";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const Report = () => {
  const [percentages, setPercentages] = useState({});
  const [loading, setLoading] = useState(true);
  const [aqiData, setAqiData] = useState(null);
  const [loadingAqi, setLoadingAqi] = useState(true);

  // Retrieve coordinates from localStorage
  const latitude = parseFloat(localStorage.getItem('lat'));
  const longitude = parseFloat(localStorage.getItem('lng'));

  // Colors for pie chart
  const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#8dd1e1', '#d0ed57', '#a4de6c'];

  // Fetch AQI data from Open-Meteo API using stored coordinates
  useEffect(() => {
    if (latitude && longitude) {
      // Request hourly pollutant values:
      // Available parameters: pm10, pm2_5, carbon_monoxide, nitrogen_dioxide, sulphur_dioxide, ozone
      fetch(`https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${latitude}&longitude=${longitude}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone`)
        .then(response => response.json())
        .then(data => {
          console.log("AQI data:", data);
          setAqiData(data);
          setLoadingAqi(false);
        })
        .catch(error => {
          console.error('Error fetching AQI data:', error);
          setLoadingAqi(false);
        });
    } else {
      console.error("Latitude and/or Longitude are not available in localStorage");
      setLoadingAqi(false);
    }
  }, [latitude, longitude]);

  // Fetch percentage data for the pie chart
  useEffect(() => {
    fetch('http://localhost:5000/calculate_percentages')
      .then(response => response.json())
      .then(data => {
        setPercentages(data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching percentages:', error);
        setLoading(false);
      });
  }, []);

  // Convert percentages object to an array for the pie chart
  const pieData = Object.entries(percentages).map(([name, value]) => ({
    name,
    value: parseFloat(value),
  }));

  // Extract latest hourly data from the API response.
  // The API returns an "hourly" object with arrays for each pollutant.
  let latestData = null;
  if (aqiData && aqiData.hourly && aqiData.hourly.time && aqiData.hourly.time.length > 0) {
    const index = 0; // Using the first entry; adjust if you need to target the current hour
    latestData = {
      time: aqiData.hourly.time[index],
      carbon_monoxide: aqiData.hourly.carbon_monoxide[index],
      nitrogen_dioxide: aqiData.hourly.nitrogen_dioxide[index],
      sulphur_dioxide: aqiData.hourly.sulphur_dioxide[index],
      ozone: aqiData.hourly.ozone[index],
      pm10: aqiData.hourly.pm10[index],
      pm2_5: aqiData.hourly.pm2_5[index],
    };
  }

  return (
    <>
      <NavBar />
      <h2 className='report-heading'>Classification Report</h2>
      <div className="report-container" style={{ padding: "2rem" }}>
        <div>
        {loading ? (
          <p>Loading land percentage data...</p>
        ) : (
          <>
            <h3 className='report-list-h'>Land Percentage Division</h3>
            <ul className='report-list'>
              {pieData.map((item) => (
                <li className='report-list' key={item.name}>
                  <strong className='report-list'>{item.name}</strong>: {item.value}%
                </li>
              ))}
            </ul>

            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={120}
                  label
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </>
        )}
        </div>
        
        {/* AQI / Air Quality Report Section */}
        <div >
          <h3 className="report-list-h">Air Quality Report</h3>
          {loadingAqi ? (
            <p>Loading AQI data...</p>
          ) : (
            <div className='report-list'>
              {latestData ? (
                <>
                  <p><strong>Time:</strong> {latestData.time}</p>
                  <p><strong>Carbon Monoxide:</strong> {latestData.carbon_monoxide} µg/m³</p>
                  <p><strong>Nitrogen Dioxide:</strong> {latestData.nitrogen_dioxide} µg/m³</p>
                  <p><strong>Sulphur Dioxide:</strong> {latestData.sulphur_dioxide} µg/m³</p>
                  <p><strong>Ozone:</strong> {latestData.ozone} µg/m³</p>
                  <p><strong>PM10:</strong> {latestData.pm10} µg/m³</p>
                  <p><strong>PM2.5:</strong> {latestData.pm2_5} µg/m³</p>
                </>
              ) : (
                <p>Unable to retrieve AQI data.</p>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default Report;
