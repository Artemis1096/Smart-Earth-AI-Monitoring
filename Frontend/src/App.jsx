import React from 'react';
import SmartCity from './pages/SmartCity';
import AiMap from './components/smart ai map/aimap';
import Explanation from "./pages/Explanation";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Router components
import LandingPage from "./pages/LandingPage"
import './App.css';
const App = () => (
  <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} /> {/* Default route */}
        <Route path="/smart-city" element={<SmartCity />} />
        <Route path="/aimap" element={<AiMap />} />
        <Route path='/WhatDoesItRepresents' element={<Explanation/>} />
      </Routes>
  </Router>
);

export default App;