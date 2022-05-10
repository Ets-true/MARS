import React from 'react'
import fireSvg from "./img/fire.svg"
import dropSvg from "./img/drop.svg"
import personSvg from "./img/person.svg"
import dop from "./img/out.svg"
import {Link} from "react-router-dom"

export default function NavBar() {
  return (
    <div className='Navbar__body'>
        <div className="logo"></div>
        <div className="component fire">
          <Link to="/fire"><img src={fireSvg} alt="" /></Link>
          {/* <div className="dot"></div> */}
          
        </div>
        <div className="component water">
        {/* <div className="dot"></div> */}
          <Link to="/water"><img src={dropSvg} alt="" /></Link>
        </div>
        <div className="component skud">
        {/* <div className="dot"></div> */}
          <Link to="/skud"><img src={personSvg} alt="" /></Link>
        </div>
        <div className="dop"><img src={dop} alt="" /></div>
    </div>
  )
}
