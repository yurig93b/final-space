const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = require("socket.io")(server, {
  cors: {
    origin: "http://localhost:8090",
    methods: ["GET", "POST"]
  }
});

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/src/index.html');
});

io.on('connection', (socket) => {
  console.log('A client is connected!');
  socket.onAny((eventName, ...args) => {
    console.log(`Broadcasting ${eventName} with ${JSON.stringify(...args)}`);
    socket.broadcast.emit(eventName, ...args);
  });
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});
