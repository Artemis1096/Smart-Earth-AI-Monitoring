import React from 'react';
import SmartCity from './pages/SmartCity';
import AiMap from './components/smart ai map/aimap';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import Router components
import LandingPage from "./pages/LandingPage"
import './App.css';
const App = () => (
  <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} /> {/* Default route */}
        <Route path="/smart-city" element={<SmartCity />} />
        <Route path="/aimap" element={<AiMap />} />
      </Routes>
  </Router>
);

export default App;