import './App.css';
import React, { Children } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


//layout pages
import Navbar from './components/Navbar/Navbar';
import TextOnly from './components/TextOnly/TextOnly';
import MyProjects from './components/MyProjects/MyProjects';
import Footer from './components/footer/Footer';

const Layout= ({children}) => (
  <div>
    <Navbar />
    {children}
    <Footer />
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<Layout> <TextOnly /> </Layout>} />
        <Route path='/MyProjects' element={<MyProjects />} />
      </Routes>
    </Router>
  );
}

export default App;
