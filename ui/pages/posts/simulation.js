import Layout from '@/components/layout';
import Rocket from '@/components/rocket';
import Link from 'next/link';
import { io } from 'socket.io-client';
import styles from '../../components/layout.module.css';
import Moon from '../../components/moon'
import React, {useEffect, useState} from 'react';
import StatusInfo from '@/components/statusInfo';
import { red } from '@mui/material/colors';

var socket = io('http://localhost:3000');

socket.on('simulation_started', function(data) {
  console.log("started Bereshit simulation");
});


socket.on('fts_activated', function(data){
  // printFlightStatus(data);
  console.log("||*****************||");
  console.log("The ship is BROKEN!!");
  console.log("||*****************||");
});

socket.on('simulation_ended', function(data){
  // printFlightStatus(data);
  console.log("****************** simulation ended ******************");
});

function showStatusOnScreen(status){

}

function printFlightStatus(status){
  console.log('Flight status:')
  // acc
  console.log('acc = ' + status.acc);
  // alt
  console.log('alt = ' + status.alt);
  // ang_relative_to_body
  console.log('ang_relative_to_body = ' + status.ang_relative_to_body);
  // distance
  console.log('distance = ' + status.distance);
  // dt
  console.log('dt = ' + status.dt);
  // fuel
  console.log('fuel = ' + status.fuel);
  // hs
  console.log('hs = ' + status.hs);
  // thrust
  console.log('thrust = ' + status.thrust);
  // time
  console.log('time = ' + status.time);
  // vehicle_ang
  console.log('vehicle_ang = ' + status.vehicle_ang);
  // vs
  console.log('vs = ' + status.vs);
  // wanted_hs
  console.log('wanted_hs = ' + status.wanted_hs);
  // wanted_thrust
  console.log('wanted_thrust = ' + status.wanted_thrust);
  // wanted_vehicle_ang
  console.log('wanted_vehicle_ang = ' + status.wanted_vehicle_ang);
  // wanted_vs
  console.log('wanted_vs = ' + status.wanted_vs);
  // weight
  console.log('weight = ' + status.weight);
  console.log('-------------------------------');
}


// function that returns the new scale size according to the rocket alt
function fScale(height){
  const scale = 1/(height/1000);
  const ans = Math.min(1, Math.max(0.1,scale))
  return ans;
}

export default function Simulation() {
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
  const [flightStatus, setFlightStatus] = useState(temp);
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
    <div className={styles.simulationPage}>
      <h1 style={{color:'white'}}>Simulation</h1>
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