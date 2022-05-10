import React from 'react'
import video from "./img/sklad.mp4"

export default function Video() {
  return (
    <video className="player" src={video} autoplay="true" loop="true"/>
  )
}
