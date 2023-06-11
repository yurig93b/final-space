import Layout from '@/components/layout';
import Link from 'next/link';
import styles from '../../components/layout.module.css';
import Rocket from '@/components/rocket';
import Moon from '@/components/moon';
import React, {useEffect, useState} from 'react';
import { io } from 'socket.io-client';
import StatusInfo from '@/components/statusInfo';

var socket = io('http://localhost:3000');

socket.on('simulation_started', function(data) {
  console.log("started Bereshit simulation");
});

// function that returns the new scale size according to the rocket alt
function fScale(height){
  const scale = 1/(height/1000);
  const ans = Math.min(1, Math.max(0.1,scale))
  return ans;
}

socket.on('simulation_ended', function(data){
  // printFlightStatus(data);
  console.log("****************** simulation ended ******************");
});


export default function Starhoper() {
  const temp = {
    "acc":0,
    "alt":0, 
    "ang_relative_to_body":0, 
    "distance":0, 
    "dt":0,
    "fuel":0, 
    "hs":0, 
    "thrust":0, 
    "time":0, 
    "vehicle_ang":0, 
    "vs":0, 
    "wanted_hs":0, 
    "wanted_thrust":0,
    "wanted_vehicle_ang":0, 
    "wanted_vs":0,  
    "weight":0};

 const [scale, setScale] = useState(1);
 const[flightStatus, setFlightStatus] = useState(temp);
 const [radius, setRadius] = useState(0);

  useEffect(() => {
    socket.on('flight_status', function(data){
      setFlightStatus(data);

      // getting the new scale for the image based on the alt
      const newScale = fScale(data.alt);
      setScale(newScale);
    });
    }, []);

    function Callback (childRadius){
      setRadius(childRadius);
    }

  return (
    <div className={styles.starhoperPage}>
      <h1 style={{color: 'white'}}>Starhoper</h1>
      <h2 style={{color: 'white'}}>
        <Link href="/" style={{color: 'white'}}>Back to menu</Link>
      </h2>

      <div className={styles.container}>
        <div className={styles.moon_div} style={{transform: `scale(${scale})`}}>
          <div className={styles.rocket_div} >
            <Rocket flightStatus={flightStatus} Radius={radius}/>
          </div>
          <Moon flightStatus={flightStatus} handleCallBack={Callback}/>
        </div>
        <StatusInfo flightStatus={flightStatus}/>
      </div>
    </div>
  );
}