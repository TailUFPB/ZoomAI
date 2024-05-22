import React, { Children } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

//layout pages
import Navbar from './components/Navbar';
import TextOnly from './components/TextOnly';
import MyProjects from './components/MyProjects';
import Footer from './components/Footer';
import Project from './pages/Zoom';
   

const Layout= ({children}) => (
  <>
    <Navbar />
    {children}
    <Footer />
  </>
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