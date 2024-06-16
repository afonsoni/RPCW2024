import React from 'react';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home'; 
import Criar from './pages/Criar';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/CriarFesta" element={<Criar/>} />
      </Routes>
    </Router>
  );
}


export default App;