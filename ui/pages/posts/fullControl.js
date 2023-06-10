import AngSlider from '@/components/angSlider';
import Rocket from '@/components/rocket';
import ThrustSlider from '@/components/thrustSlider';
import React, {useEffect, useState,setState} from 'react';
import Link from 'next/link';
import { io } from 'socket.io-client';
import styles from '../../components/layout.module.css';
import Moon from '@/components/moon';
import Stack from '@mui/material/Stack';
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

export default function FullControl() {
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

    const temp2 = {
      "wanted_thrust" : 0.0,
      "wanted_vehicle_ang" : 0.0
    }
    

  const [scale, setScale] = useState(1);
  const [flightStatus, setFlightStatus] = useState(temp);
  const [radius, setRadius] = useState(0);
  const [userValues, setUserValues] = useState(temp2);
  
  
  useEffect(() => {
    socket.on('flight_status', function(data){
      setFlightStatus(data);

      // getting the new scale for the image based on the alt
      const newScale = fScale(data.alt);
      setScale(newScale);
    });

    socket.on('simulation_ended', function(data){
      // printFlightStatus(data);
      console.log("****************** simulation ended ******************");
    });

    socket.on('fts_activated', function(data){
      console.log("||*****************||");
      console.log("The ship is BROKEN!!");
      console.log("||*****************||");
    });
    
    }, []);

    // function to handle the radius callback
    function RadiusCallback (childRadius){
      setRadius(childRadius);
    }

    // functions to handle the angle
    function updatePython(){
      // console.log("wanted angle = " + userValues.wanted_vehicle_ang);
      socket.emit("new_control_info", userValues);
    }

    function handleAngChange(newAng){
      // console.log("new value = " + newAng);
      if (typeof newAng === 'number') {
        
        // update the state
        setUserValues(prevState => ({
          ...prevState,
          "wanted_vehicle_ang": newAng,
        }));

        // we want to update the python file 10 times to change the angle to the desired value
        const intervalId = setInterval(updatePython, 100);

        setTimeout(() => {
          clearInterval(intervalId);
          console.log('Interval stopped.');
        }, 1000);
      }
    };


    function handleThrustChange(newThrust){
      if (typeof newThrust === 'number'){
        setUserValues(prevState => ({
          ...prevState,
          "wanted_thrust": newThrust,
        }));

        const intervalId = setInterval(updatePython, 100);

        setTimeout(() => {
          clearInterval(intervalId);
          console.log('Interval stopped.');
        }, 1000);
      }
    };
    
  return (
    <div className={styles.manualPage}>
      <h1 style={{color: 'white'}}>Manual control</h1>
      <h2 style={{color: 'white'}}>
        <Link href="/" style={{color: 'white'}}>Back to menu</Link>
      </h2>
      <div className={styles.container}>
        <div className={styles.moon_div} style={{transform: `scale(${scale})`}}>
          <div className={styles.rocket_div} >
            <Rocket flightStatus={flightStatus} Radius={radius}/>
          </div>
          <Moon flightStatus={flightStatus} handleCallBack={RadiusCallback}/>
        </div>
        <StatusInfo flightStatus={flightStatus}/>
      </div>

      <div>
      <Stack style={{bottom:`15px`,
       position:'fixed',
        left:`40%`,
         height:`20vh`,
          // backgroundColor:'#ff5252',
          width:`100vw`}} spacing={0.1}>
        <AngSlider onChange={handleAngChange}/>
        <ThrustSlider onChange={handleThrustChange}/>
      </Stack>
      </div>
    </div>
  );
}