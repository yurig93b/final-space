import React, {useState,useLayoutEffect, useRef} from 'react';
import styles from './moon.module.css';
import Rocket from './rocket';
import Image from 'next/image';


function getRadius(){
    const moonRef = document.getElementById('moonId');
    const { width } = moonRef.getBoundingClientRect();
    // console.log("width = " + width);
    return width/2;
}

const Moon = ({flightStatus, handleCallBack}) => {
    
    useLayoutEffect(() => {
        handleCallBack(getRadius());
      }, [handleCallBack]);
    
    
    return (
    <div id="moonId" className={styles.moon}>
        <Image
            src="/images/moon9.png"
            fill={true}
            alt='moon'
            />
    </div>);
}

export default Moon;