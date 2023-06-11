import Head from 'next/head';
import Link from 'next/link';
import Layout from '@/components/layout';
import { io } from 'socket.io-client';
import styles from '../components/layout.module.css'



const socket = io('http://localhost:3000');

const handleClickSimulation = (event) => {
    // Send a message to the server
    socket.emit("start_simulation", "bereshit");
  };

const handleClickController = (event) => {
    // Send a message to the server
    socket.emit("start_simulation", "manual_control");
};

const handleClickStarhoper = (event) => {
    // Send a message to the server
    socket.emit("start_simulation", "starhoper");
};
  
export default function Home() {
  return (
    <div className={styles.index_page_div}>
        <div>
            <h1 className={styles.index_title}>New space</h1>
            <h2 className={styles.index_sub_title}>Final task</h2>
        </div>
        <div>
            <h2 className={styles.simulation_text}>
                <Link href="/posts/simulation" onClick={handleClickSimulation}>Simulation</Link>
            </h2>
            <h2 className={styles.fullcontrol_text}>
                <Link href="/posts/fullControl" onClick={handleClickController}>Manual control</Link>
            </h2>
            <h2 className={styles.starhoper_text}>
                <Link href="/posts/starhoper" onClick={handleClickStarhoper}>Starhoper</Link>
            </h2>
        </div>
        
    </div>
  );
}