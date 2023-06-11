import Image from 'next/image';
import React, {useState} from 'react';
import styles from './rocket.module.css';

function Fire({op}){
    return (<Image 
        src="/images/fire.png" // Route of the image file
        height={64}
        width={64} 
        alt='fire'
        style={{opacity:`${op}`}}
    />);
}

function getTop(alt){
    const ans = Math.min(1300, Math.max(0,alt/10))
    return -ans + 40;
}

function getLeftValue(radius, ang, alt){
        console.log("current radius of the moon: " + radius);
        console.log("current ang: " + ang);
        console.log("current alt: " + alt);
        const ans = Math.cos(ang)*(alt/1000)+radius+64;
        console.log("*** Left value is: " + ans);
        return ans;
    }

const Rocket = ({flightStatus, Radius}) => {
    return (
        <div className={styles.rocket_container} 
            style={{top:`${getTop(flightStatus.alt)}px`,
                    left:`${getLeftValue(Radius, flightStatus.ang_relative_to_body, flightStatus.alt)}px`,
                    transform: `rotate(${-(flightStatus.vehicle_ang)}deg)`}}>
            <div className={styles.rocket}>
                <Image 
                    src="/images/Rocket.png"
                    height={64}
                    width={64}
                    alt='rocket'
                />
            </div>
            <div className={styles.fire}>
                <Fire op={flightStatus.thrust}/>
            </div>
        </div>
    );
}

export default Rocket;