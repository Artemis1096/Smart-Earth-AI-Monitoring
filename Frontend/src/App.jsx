import React from 'react';
import SmartCity from './pages/SmartCity';
import AiMap from './components/smart ai map/aimap';
import Explanation from "./pages/Explanation";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Router components
import LandingPage from "./pages/LandingPage"
import './App.css';
import Aqi from "./components/Aqi"
import Report from "./components/report"
const App = () => (
  <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} /> {/* Default route */}
        <Route path="/smart-city" element={<SmartCity />} />
        <Route path="/aimap" element={<AiMap />} />
        <Route path='/WhatDoesItRepresents' element={<Explanation/>} />
        <Route path='/aqi' element={<Aqi />} />
        <Route path='/report' element={<Report />} />
      </Routes>
  </Router>
);

export default App;