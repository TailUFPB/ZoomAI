import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

//layout pages
import Navbar from './components/Navbar';
import AllProjects from './components/MyProjects';
import Footer from './components/Footer';
import Project from './pages/Zoom';
import Home from './pages/Home';


const Layout= ({children}) => (
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
               </Routes>
         </BrowserRouter>
      </div>
   );
}

export default App;
