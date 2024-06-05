import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

//layout pages
import Navbar from './components/Navbar';
import AllProjects from './components/MyProjects';
import Footer from './components/Footer';
import Project from './pages/Zoom';
import Home from './pages/Home';
import About from './pages/About';

const Layout = ({ children }) => (
   <>
      <Navbar />
      {children}
      <Footer />
   </>
);


function App() {
   return (
      <div style={{ backgroundColor: 'black' }}>
         <BrowserRouter>
            <Routes>
               <Route path="/" element={<Layout> <Home /> </Layout>} />
               <Route path='/projects' element={<AllProjects />} />
               <Route path="/zoom" element={<Project />} />
               <Route path="/about" element={<Layout><About /></Layout>} />
            </Routes>
         </BrowserRouter>
      </div>
   );
}

export default App;
