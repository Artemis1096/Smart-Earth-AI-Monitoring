import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  // Update to import Routes from react-router-dom
import CoordsFinder from './components/smart ai map/coordsfinder';
import AiMap from './components/smart ai map/aimap';
import { Footer, Possibility, Features, What, Header } from './containers';
import { Navbar } from './components';

import './App.css';

const App = () => (
  <div className="App">
    <div className="gradient__bg">
      <Navbar />
      <Header />
    </div>
    <What />
    <Features />
    <Possibility />
    <Footer />
  </div>
);

export default App;