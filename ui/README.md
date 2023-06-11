This is the frontend part of the final project in New Space course.

## Getting Started
First, install all dependencies by running:
```bash
npm install
```
After that to run the application write:
```bash
npm run dev
```
A url ([http://localhost:8090](http://localhost:8090)) supposed to appear on the console, copy and paste it on your preferred browser.

## About
The frontend written in JavaScript with [Next.js framework](https://nextjs.org/).

The main purpose of this part of the project is to represent the current status of the rocket corresponding to the moon and to other factors in 2D graphics.

The user have the option to control the rocket by using 2 sliders - one for the angle of the rocket and the other for the thrust:

![image](https://github.com/yurig93b/final-space/assets/74859686/3ff3982a-6dbd-4713-8c84-ab4b65c90d50)

Also the user can see the current flight status on the right side of the screen:

![image](https://github.com/yurig93b/final-space/assets/74859686/bd668952-e5db-49ef-9508-5803d69694e9)

## How it works
First the user decide which screen he wants to open.(Simulation, Manual control, Starhoper)

After that a message from the frontend is sent via a websocket([Socket.io](https://socket.io/)) to the backend and tells it what simulation to run.

Then the backend send data that contains the flight status 10 times per second to the frontend.

