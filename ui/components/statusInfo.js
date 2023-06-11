import React, {useState} from "react";
import styles from "./statusInfo.module.css";

const StatusInfo = ({flightStatus}) => {
    const [value, setValue] = useState(null);

    return (
        <div className={styles.container}>
             <h1 className={styles.title}>status info</h1>
             <h4 className={styles.info}>hs = {(flightStatus.hs).toFixed(4)}</h4>
             <h4 className={styles.info}>vs = {(flightStatus.vs).toFixed(4)}</h4>
             <h4 className={styles.info}>thrust = {(flightStatus.thrust).toFixed(4)}</h4>
             <h4 className={styles.info}>alt = {(flightStatus.alt).toFixed(4)}</h4>
             <h4 className={styles.info}>acc = {(flightStatus.acc).toFixed(4)}</h4>
             <h4 className={styles.info}>distance = {(flightStatus.distance).toFixed(4)}</h4>
             <h4 className={styles.info}>fuel = {(flightStatus.fuel).toFixed(4)}</h4>
             <h4 className={styles.info}>ang = {(flightStatus.vehicle_ang).toFixed(4)}</h4>
             <h4 className={styles.info}>weight = {(flightStatus.weight).toFixed(4)}</h4>
        </div>
    );
};

export default StatusInfo;

