import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import NavBar from "./navbar/Navbar";

const Report = () => {
  const [percentages, setPercentages] = useState({});
  const [loading, setLoading] = useState(true);

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

  return (
    <>
      <NavBar />
      <div className="report-container" style={{ padding: "2rem" }}>
        <h2>Classification Report</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <ul>
            {Object.entries(percentages).map(([category, percent]) => (
              <li key={category}>
                <strong>{category}</strong>: {percent}
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
};

export default Report;
