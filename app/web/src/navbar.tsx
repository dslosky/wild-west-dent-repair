import './navbar.css'
import logo from "./assets/resized-logo.jpg"
import menuOpenSvg from "./assets/menu.svg"
import menuCloseSvg from "./assets/x.svg"

import { Link } from "react-router-dom";
import { useState } from 'react';


function Navbar() {
  const [show, setShow]: any = useState(false);

  const openMenuIcon = <img src={menuOpenSvg} />;

  const closeMenuIcon = <img src={menuCloseSvg} />;

  const menuIcon = show ? closeMenuIcon : openMenuIcon;

  return (
    <div className="navbar-container">

        <img className="my-logo" src={logo} />
        <img className="relative-logo" src={logo} />

        <nav className={show ? "show" : ""}>
            <ul>
                <li className="drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
                    <Link to="/" onClick={()=>setShow(false)}>
                        Home
                    </Link>
                </li>
                <li className="drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
                    <Link to="/About" onClick={()=>setShow(false)}>
                        Our Story
                    </Link>
                </li>
                <li className="drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
                    <Link to="/Contact" onClick={()=>setShow(false)}>
                        Contact
                    </Link>
                </li>
                <li className="drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
                    <Link to="https://calendly.com/wild-west-dent-repair/consultation" target="_blank" rel="noopener noreferrer" >
                        Schedule
                    </Link>
                </li>
            </ul>
        </nav>

        <div className={"menu-icon".concat(show ? " x" : "")} onClick={()=>setShow(!show)}>{menuIcon}</div>
    </div>
  )
}

export default Navbar

