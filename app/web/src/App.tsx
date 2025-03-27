import './App.css'
import { Route, Routes, useLocation } from "react-router-dom";
import Contact from "./contact"
import Home from "./home"
import About from "./about"
import Navbar from './navbar';

import image from "./assets/WWDR-09.jpg"
import aboutImage from "./assets/WWDR-15.jpg"

function App() {
  const aboutPage = useLocation().pathname == "/About"
  const backgroundImg = aboutPage ? aboutImage : image

  return (
    <div className="app">
      <div className="background-img">

        <img className={aboutPage?"aboutPage":""} src={backgroundImg} />
        <div className="shadow"></div>
      </div>

      <Navbar></Navbar>
      
      <div className="rendered">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/About" element={<About />} />
          <Route path="/Contact" element={<Contact />} />
        </Routes>
      </div>
    </div>
  )
}

export default App
