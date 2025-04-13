import React from 'react';

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