import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Project from './pages/Zoom';

function App() {
   return (
      <div>
         <BrowserRouter>
            <Routes>
               <Route path="/" element={<Home />} />
               <Route path="/zoom" element={<Project />} />
            </Routes>
         </BrowserRouter>
      </div>
   );
}

export default App;