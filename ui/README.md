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

The main purpose of this part of the project is to represent the current status of the flight in 2D graphics.
![image](https://github.com/yurig93b/final-space/assets/74859686/9e392d1d-c38a-446b-9c9c-50fbe5c5c2cc)

The user have the option to control the rocket by using 2 sliders - one for the angle of the rocket and the other for the thrust:

![image](https://github.com/yurig93b/final-space/assets/74859686/3ff3982a-6dbd-4713-8c84-ab4b65c90d50)

Also the user can see the current flight status on the right side of the screen:

![image](https://github.com/yurig93b/final-space/assets/74859686/bd668952-e5db-49ef-9508-5803d69694e9)

## Calculations
1)To show the moon and the rocket for the whole simulation we thought about the next idea:

When the rocket is far away from the moon we will decrease their size, and when the rocket is closer then we increase their size.

To do this we used the next logic: 

![image](https://github.com/yurig93b/final-space/assets/74859686/416db88b-1b63-4d12-89b5-963056fda489)

We set the scale (value between 0 to 1) to be 1 divide by the (rocket.altitude/1000)

And then we bound it to our limits, that means if the rocket is far away the minimum scale will be 0.1.

And if the rocket is very close to the moon then we set the scale to be 1.

That way we keep the rocket and the moon visible for the whole flight simulation.

The Moon and the Rocket are inside a <div> element with size of 400x400 px, so we change the scale of this div to the calculation's result.
  
2)To position the rocket right in the middle of the moon we had to change varius positions.
  
We set the moon values to be:
```bash
height = 200px
width = 200px
left = 100px
bottom = 100px
```
That way we put the Moon in the middle of the div that mentioned above.
  
The rocket is a little bit more complicated, we want it to be right on the moon, so we set it's values to be:
```bash
left = 164px
bottom = 40px
```
This values takes into account the size of the rocket (including the fire effect).
  
3)To position the rocket in the right place (x-axis) we had to do the next calculation:
```bash
  const ans = Math.cos(ang)*(alt/1000)+radius+64;
```
The rocket and the moon defines a circle (the distance between the rocket to the moon is the radius).
  
We multiply the angle (of the position we want to place the rocket on) with the distance of the rocket from the moon (divided by 1000) and adding the radius (because it's a circle) and adding 64 which is the height size of the upper part of the rocket. 

## How it works
First the user decide which screen he wants to open.(Simulation, Manual control, Starhoper)

After that a message from the frontend is sent via a websocket([Socket.io](https://socket.io/)) to the backend and tells it what simulation to run.

Then the backend send data that contains the flight status 10 times per second to the frontend.

Each page process the data and transfer the right data to the right component, and each component will be updataed and shown on the screen.

To make it more understandable we will explain each page:


