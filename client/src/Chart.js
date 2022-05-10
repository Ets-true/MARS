import React, {useState} from 'react'
// import Waterlevel from './App'



export default function Chart({Waterlevel}) {

    // function changeColumns(){
    //     var obj = document.querySelectorAll(".filling")
    //     var array1 = ['50px', '100px', '150px', '200px', '250px', '300px', '350px', '400px', '450px']
    //     var array2 = ['0px', '0px', '0px', '0px', '0px', '0px', '0px', '0px', '0px']
    //     var array3 = ['450px', '400px', '350px', '300px', '250px', '200px', '150px', '100px', '50px']
    //     var array4 = ['0px', '0px', '0px', '0px', '0px', '0px', '0px', '0px', '0px']
    //     var array5 = ['500px', '500px', '500px', '500px', '500px', '500px', '500px', '500px', '500px']
    //     var mass
    //     var arrayGlobal = [array1, array2, array3, array4, array5]
    //     var step = 0;
        
    //     function redraw(){
    //         obj.forEach(function(item, i, arr) {
    //             item.style.height = arrayGlobal[step][i];
    //         })
    //         step++
    //         if(step < arrayGlobal.length){
    //             setTimeout(() => {
    //                 redraw()
    //             }, 2000);
    //         }
    //     }
    //     // redraw()
        
    // }
    // document.addEventListener("DOMContentLoaded",changeColumns );

    function redraw2(){
        var obj = document.querySelectorAll(".capacity")
        var objWrap = document.querySelector(".XY__body_wrapper")

        obj[0].style.opacity = 0;
        obj.forEach(function(item, i, arr) {
            if(i>0){
                 item.style.transform = "translateX(-120px)";
            }
           
        })
        var newCapacity = document.createElement("div");
        newCapacity.setAttribute("class", "capacity");

        var newFilling = document.createElement("div");
        newFilling.setAttribute("class", "filling NewFilling");

        newCapacity.appendChild(newFilling);
        objWrap.appendChild(newCapacity);
        var obj = document.querySelectorAll(".capacity")
    }

    var arrTestStart = [[100,"10:20:00"], [150,"10:20:05"], [200,"10:20:10"], [250,"10:20:15"], [300,"10:20:20"], [350,"10:20:25"], [400,"10:20:30"], [450,"10:20:35"], [500,"10:20:40"], [550,"10:20:45"]]
    const [arrayState, changeState] = useState(arrTestStart);
    
    let arrTestWork = arrayState;
    // alert(arrayState)

    arrTestWork.splice(0, 1)
    arrTestWork.push(Waterlevel[1][0])

    function changeColumns(){
        var obj = document.querySelectorAll(".filling")
        var time = document.querySelectorAll(".time")
        obj.forEach(function(item, i, arr) {
            item.style.height = arrayState[i][0] + "px";
            if(arrayState[i][0]>=470){
                item.style.backgroundColor = "red"
                item.style.opacity = "1"
            }
            time[i].innerHTML = arrayState[i][1]
        }) 
    }
    document.addEventListener("DOMContentLoaded",changeColumns );
    changeColumns()
  
    
  return (
    <div className='chart__body'>
        <div className="chart__title">Пожарная безопасность</div>
        <div className="chart__X"></div>
        <div className="chart__Y"></div>
        <div className="limit">
            Допустимый предел
            <div className="limit__line"></div>
            <div className="limit__line_punctir"></div>
        </div>
        <div className="XY__body">
            <div className="XY__body_wrapper">
                <div className="capacity">
                    <div className="filling _1"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _2"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _3"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _4"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _5"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _6"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _7"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _8"></div>
                    <div className="time"></div>
                </div>
                <div className="capacity">
                    <div className="filling _9"></div>
                    <div className="time"></div>
                </div>
            </div>
        </div>
        {/* <button onClick={ChangeS}></button> */}
    </div>
  )
}
