import React, { useState, createContext } from 'react';
import NavBar from './NavBar'
import Chart from './Chart'
import Skud from './Skud'
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import phone from './img/phone.svg'
import Water from './Water';
import Moment from "react-moment";



function App() {

  const [value, onChange] = useState(new Date());

  const [Waterlevel, setWaterLevel] = useState([[0, "00:00:00"], [100, "00:00:00"], [2, "00:00:00"], [3, "00:00:00"]]);
  console.log(Waterlevel[1][0])
  const newConst = [[0, "00:00:00"], [100, "00:00:00"], [2, "00:00:00"], [3, "00:00:00"]]
  var otv;

  function subscribe() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://0meka0.hopto.org/", true);

    xhr.onload = function () {
      otv = JSON.parse(this.responseText)
      newConst[1][0] = otv.Illumination * 10 - 3000
      handleClick()
      setTimeout(subscribe, 500);
    }
    xhr.onerror = xhr.onabort = function () {
      newConst[1][0] = 100
      handleClick()
      console.log(newConst)
      console.log(Waterlevel)
      setTimeout(subscribe, 500);
    }
    xhr.send('');
  }
  // subscribe();
  // document.addEventListener("DOMContentLoaded", subscribe);
  function handleClick() {
    setWaterLevel(newConst)
  }

  return (
    <div className="main">
      <Router>
        <NavBar />
        <div className="clock">
          <Moment format="HH:mm:ss" interval={1000} />
          {/* <Moment format="hh:mm:ss DD.MM.YYYY" durationFromNow /> */}
        </div>
        <div className="chart">
          <Routes>
            <Route path="/fire" element={<Chart Waterlevel={Waterlevel} />} />
            <Route path="/water" element={<Water/>} />
            <Route path="/skud" element={<Skud/>} />
          </Routes>
        </div>
        <div className="calendarPersonal">
          <Calendar onChange={onChange} value={value} />
        </div>
        <div className="buttonPersonal buttonCalling1">
          <div className="phone__icon"><img src={phone} alt=""></img></div>
          Помещение
        </div>
        <div className="buttonPersonal buttonReaction">Двери</div>
        <div className="buttonPersonal buttonCalling2">
          <div className="phone__icon"><img src={phone} alt=""></img></div>
          Служба 112
        </div>
        <div className="developers">
          powered by<div className="department"><a href="https://departmentview.ru" target="_blank">department</a></div>
        </div>
        
      </Router>
    </div>
  )
}

export default App;

