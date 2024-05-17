const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files from the public directory
app.use(express.static('public'));

// Event listener for new connections
io.on('connection', socket => {
    console.log('A user connected');

    // Event listener for incoming messages
    socket.on('message', data => {
        console.log('Message received:', data);

        // Broadcast the message to all connected clients
        io.emit('message', data);
    });

    // Event listener for disconnections
    socket.on('disconnect', () => {
        console.log('User disconnected');
    });
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
