const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
    methods: ['GET', 'POST']
  }
});

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Store connected users
const users = new Map();
const rooms = new Map();

// Room management
const defaultRooms = ['general', 'random', 'tech'];
defaultRooms.forEach(room => rooms.set(room, new Set()));

// Chat history (in-memory, limited to 100 messages per room)
const chatHistory = new Map();
defaultRooms.forEach(room => chatHistory.set(room, []));

// Socket.IO connection handling
io.on('connection', (socket) => {
  console.log(`User connected: ${socket.id}`);

  // Send chat history on connection
  defaultRooms.forEach(room => {
    socket.emit('chat history', {
      room,
      messages: chatHistory.get(room)
    });
  });

  // Handle user joining
  socket.on('join', ({ username, room }) => {
    if (!username) {
      socket.emit('error', { message: 'Username is required' });
      return;
    }

    const userRoom = room || 'general';

    // Leave previous room if any
    if (users.has(socket.id)) {
      const oldUser = users.get(socket.id);
      if (rooms.has(oldUser.room)) {
        rooms.get(oldUser.room).delete(socket.id);
        io.to(oldUser.room).emit('user left', {
          username: oldUser.username,
          room: oldUser.room
        });
      }
    }

    // Join new room
    socket.join(userRoom);
    users.set(socket.id, { username, room: userRoom });

    if (!rooms.has(userRoom)) {
      rooms.set(userRoom, new Set());
    }
    rooms.get(userRoom).add(socket.id);

    // Notify room members
    io.to(userRoom).emit('user joined', {
      username,
      room: userRoom,
      users: Array.from(rooms.get(userRoom).size)
    });

    // Send room list update
    io.emit('room list', Array.from(rooms.keys()));

    console.log(`${username} joined ${userRoom}`);
  });

  // Handle chat messages
  socket.on('chat message', ({ message, room }) => {
    const user = users.get(socket.id);
    if (!user) {
      socket.emit('error', { message: 'Please join first' });
      return;
    }

    const messageData = {
      id: Date.now(),
      username: user.username,
      message: message.trim(),
      room: room || user.room,
      timestamp: new Date().toISOString()
    };

    // Store in history
    const history = chatHistory.get(messageData.room) || [];
    history.push(messageData);
    if (history.length > 100) history.shift();
    chatHistory.set(messageData.room, history);

    // Broadcast to room
    io.to(messageData.room).emit('chat message', messageData);
  });

  // Handle private messages
  socket.on('private message', ({ to, message }) => {
    const user = users.get(socket.id);
    const targetSocket = Array.from(users.entries())
      .find(([id, u]) => u.username === to)?.[0];

    if (!user) {
      socket.emit('error', { message: 'Please join first' });
      return;
    }

    if (!targetSocket) {
      socket.emit('error', { message: 'User not found' });
      return;
    }

    const messageData = {
      id: Date.now(),
      from: user.username,
      to,
      message: message.trim(),
      timestamp: new Date().toISOString()
    };

    socket.emit('private message', messageData);
    io.to(targetSocket).emit('private message', messageData);
  });

  // Handle typing indicator
  socket.on('typing', () => {
    const user = users.get(socket.id);
    if (user) {
      socket.to(user.room).emit('user typing', { username: user.username });
    }
  });

  // Handle stop typing
  socket.on('stop typing', () => {
    const user = users.get(socket.id);
    if (user) {
      socket.to(user.room).emit('user stopped typing', { username: user.username });
    }
  });

  // Handle room switching
  socket.on('switch room', (newRoom) => {
    const user = users.get(socket.id);
    if (!user) return;

    // Leave old room
    socket.leave(user.room);
    if (rooms.has(user.room)) {
      rooms.get(user.room).delete(socket.id);
      io.to(user.room).emit('user left', {
        username: user.username,
        room: user.room
      });
    }

    // Join new room
    socket.join(newRoom);
    user.room = newRoom;

    if (!rooms.has(newRoom)) {
      rooms.set(newRoom, new Set());
    }
    rooms.get(newRoom).add(socket.id);

    // Notify new room
    io.to(newRoom).emit('user joined', {
      username: user.username,
      room: newRoom,
      users: Array.from(rooms.get(newRoom).size)
    });

    // Send history for new room
    socket.emit('chat history', {
      room: newRoom,
      messages: chatHistory.get(newRoom) || []
    });
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    const user = users.get(socket.id);
    if (user) {
      if (rooms.has(user.room)) {
        rooms.get(user.room).delete(socket.id);
        io.to(user.room).emit('user left', {
          username: user.username,
          room: user.room
        });
      }
      users.delete(socket.id);
    }
    console.log(`User disconnected: ${socket.id}`);
  });
});

// Get rooms API
app.get('/api/rooms', (req, res) => {
  const roomList = Array.from(rooms.entries()).map(([name, members]) => ({
    name,
    users: members.size
  }));
  res.json(roomList);
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    users: users.size,
    rooms: rooms.size
  });
});

const PORT = process.env.PORT || 3003;
server.listen(PORT, () => {
  console.log(`Chat server running on http://localhost:${PORT}`);
});
