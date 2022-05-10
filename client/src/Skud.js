import React from 'react'
// import video from "./img/sklad.mp4"
import Video from "./Video"
// import "node_modules/video-react/dist/video-react.css";
// import { Player } from 'video-react';

export default function Skud() {
    return (
        <div className='skud__body'>
            <div className="chart__title skud__title">Контроль доступа</div>
            <div className="camera">
                <div className="mask"></div>
                <Video />
            </div>
            <div className="camera"></div>
            <div className="camera"></div>
            <div className="camera"></div>
        </div>
    )
}
