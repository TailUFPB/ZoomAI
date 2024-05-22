import './App.css';
import React, { Children } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import React from 'react';


//layout pages
import Navbar from './components/Navbar/Navbar';
import TextOnly from './components/TextOnly/TextOnly';
import MyProjects from './components/MyProjects/MyProjects';
import Footer from './components/footer/Footer';
import Project from './pages/Zoom';


const Layout= ({children}) => (
  <div>
    <Navbar />
    {children}
    <Footer />
  </div>
);


function App() {
   return (
      <div>
         <BrowserRouter>
            <Routes>
              <Route path="/" element={<Layout> <TextOnly /> </Layout>} />
              <Route path='/projects' element={<MyProjects />} />
              <Route path="/zoom" element={<Project />} />
            </Routes>
         </BrowserRouter>
      </div>
   );
}

export default App;