import React from 'react'
import skladImg from './img/sklad2.jpg'

export default function Water() {
    function lightUp(){
        var points = document.querySelectorAll(".point")
        points[2].style.backgroundColor = "red"
    }
    function lightDown(){
        var points = document.querySelectorAll(".point")
        points[2].style.backgroundColor = "grey"
    }
  return (
    <div className='waterBody'>
        <div className="chart__title water__title">Герметичность</div>
        <img src={skladImg} alt="" className='waterImg'/>
        <div className="point p1"></div>
        <div className="point p2"></div>
        <div className="point p3"></div>
        <div className="point p4"></div>
        <div className="point p5"></div>
        <button onClick={lightUp}></button>
        <button onClick={lightDown}></button>
    </div>
  )
}
