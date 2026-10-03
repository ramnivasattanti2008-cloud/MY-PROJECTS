import React, { useState, useEffect, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

const API_URL = 'http://localhost:5001';
const socket: Socket = io(API_URL, { transports: ['websocket', 'polling'] });

interface Message {
  id?: number;
  username: string;
  content: string;
  room: string;
  timestamp: string;
  system?: boolean;
}

interface Room {
  id: number;
  name: string;
  created_at: string;
}

export default function App() {
  const [joined, setJoined] = useState(false);
  const [username, setUsername] = useState('');
  const [selectedRoom, setSelectedRoom] = useState('general');
  const [rooms, setRooms] = useState<Room[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [newRoomName, setNewRoomName] = useState('');
  const [showCreateRoom, setShowCreateRoom] = useState(false);
  const [connected, setConnected] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    fetch(`${API_URL}/api/rooms`)
      .then(r => r.json())
      .then(d => { if (d.success) setRooms(d.data); })
      .catch(() => {});

    socket.on('connect', () => setConnected(true));
    socket.on('disconnect', () => setConnected(false));
    socket.on('message', (msg: Message) => {
      setMessages(prev => [...prev, msg]);
    });
    return () => {
      socket.off('connect');
      socket.off('disconnect');
      socket.off('message');
    };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const joinRoom = useCallback((room: string, name: string) => {
    if (!name.trim()) return;
    socket.emit('leave', { room: selectedRoom, username });
    socket.emit('join', { room, username: name });
    setSelectedRoom(room);
    setUsername(name);
    setJoined(true);
    setMessages([]);
    fetch(`${API_URL}/api/messages/${room}`)
      .then(r => r.json())
      .then(d => { if (d.success) setMessages(d.data); })
      .catch(() => {});
    setTimeout(() => inputRef.current?.focus(), 100);
  }, [selectedRoom, username]);

  const sendMessage = useCallback(() => {
    if (!input.trim() || !joined) return;
    socket.emit('message', { room: selectedRoom, username, content: input });
    setInput('');
    inputRef.current?.focus();
  }, [input, selectedRoom, username, joined]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const createRoom = () => {
    const name = newRoomName.trim().toLowerCase();
    if (!name) return;
    fetch(`${API_URL}/api/rooms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setRooms(prev => [...prev, d.data]);
          setNewRoomName('');
          setShowCreateRoom(false);
          joinRoom(name, username);
        } else {
          alert(d.error);
        }
      })
      .catch(() => alert('Failed to create room'));
  };

  const formatTime = (ts: string) => {
    try {
      const d = new Date(ts);
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch { return ts; }
  };

  if (!joined) {
    return (
      <div style={styles.container}>
        <div style={styles.joinCard}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>&#128172;</span>
            <h1 style={styles.title}>Chat Room</h1>
          </div>
          <p style={styles.subtitle}>Join a room and start chatting</p>
          <div style={styles.statusBar}>
            <span style={{ ...styles.statusDot, background: connected ? '#22c55e' : '#ef4444' }} />
            {connected ? 'Connected' : 'Connecting...'}
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Your Name</label>
            <input
              style={styles.input}
              type="text"
              placeholder="Enter your name..."
              value={username}
              onChange={e => setUsername(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && joinRoom(selectedRoom, username)}
              maxLength={30}
            />
          </div>
          <div style={styles.formGroup}>
            <label style={styles.label}>Choose a Room</label>
            <div style={styles.roomGrid}>
              {rooms.map(room => (
                <button
                  key={room.id}
                  style={{
                    ...styles.roomBtn,
                    ...(selectedRoom === room.name ? styles.roomBtnActive : {}),
                  }}
                  onClick={() => setSelectedRoom(room.name)}
                >
                  # {room.name}
                </button>
              ))}
            </div>
          </div>
          <button
            style={styles.primaryBtn}
            onClick={() => joinRoom(selectedRoom, username)}
            disabled={!username.trim() || !connected}
          >
            Join Room
          </button>
          <p style={styles.hint}>Multiple rooms available: general, tech, random, help</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <div style={styles.chatLayout}>
        <div style={styles.sidebar}>
          <div style={styles.sidebarHeader}>
            <h2 style={styles.sidebarTitle}>Rooms</h2>
            <button style={styles.addRoomBtn} onClick={() => setShowCreateRoom(!showCreateRoom)}>+</button>
          </div>
          {showCreateRoom && (
            <div style={styles.createRoomForm}>
              <input
                style={styles.createRoomInput}
                type="text"
                placeholder="room-name"
                value={newRoomName}
                onChange={e => setNewRoomName(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && createRoom()}
              />
              <button style={styles.createBtn} onClick={createRoom}>Create</button>
            </div>
          )}
          <div style={styles.roomList}>
            {rooms.map(room => (
              <button
                key={room.id}
                style={{
                  ...styles.sidebarRoom,
                  ...(selectedRoom === room.name ? styles.sidebarRoomActive : {}),
                }}
                onClick={() => {
                  socket.emit('leave', { room: selectedRoom, username });
                  joinRoom(room.name, username);
                }}
              >
                # {room.name}
              </button>
            ))}
          </div>
          <div style={styles.sidebarFooter}>
            <div style={styles.userInfo}>
              <span style={styles.userDot} />
              <span>{username}</span>
            </div>
            <button style={styles.leaveBtn} onClick={() => { socket.emit('leave', { room: selectedRoom, username }); setJoined(false); setMessages([]); }}>
              Leave
            </button>
          </div>
        </div>
        <div style={styles.chatMain}>
          <div style={styles.chatHeader}>
            <span style={styles.hashIcon}>#</span>
            <span style={styles.roomTitle}>{selectedRoom}</span>
            <span style={{ ...styles.statusDot, background: connected ? '#22c55e' : '#ef4444', marginLeft: 8 }} />
          </div>
          <div style={styles.messagesArea}>
            {messages.map((msg, i) => (
              <div key={msg.id || i} style={{ ...styles.message, ...(msg.system ? styles.systemMessage : {}) }}>
                {!msg.system && (
                  <div style={styles.messageHeader}>
                    <span style={styles.messageUser}>{msg.username}</span>
                    <span style={styles.messageTime}>{formatTime(msg.timestamp)}</span>
                  </div>
                )}
                <div style={styles.messageContent}>{msg.content}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div style={styles.inputArea}>
            <input
              ref={inputRef}
              style={styles.chatInput}
              type="text"
              placeholder={`Message #${selectedRoom}`}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              maxLength={500}
            />
            <button style={styles.sendBtn} onClick={sendMessage} disabled={!input.trim()}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', background: '#0f172a', color: '#e2e8f0', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' },
  joinCard: { maxWidth: 440, margin: '80px auto', padding: 40, background: '#1e293b', borderRadius: 16, boxShadow: '0 25px 50px rgba(0,0,0,0.5)' },
  logo: { display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 },
  logoIcon: { fontSize: 36 },
  title: { fontSize: 28, fontWeight: 700, color: '#f1f5f9', margin: 0 },
  subtitle: { color: '#94a3b8', marginBottom: 24 },
  statusBar: { display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, color: '#94a3b8', marginBottom: 24 },
  statusDot: { width: 8, height: 8, borderRadius: '50%' },
  formGroup: { marginBottom: 20 },
  label: { display: 'block', fontSize: 13, fontWeight: 600, color: '#94a3b8', marginBottom: 8, textTransform: 'uppercase', letterSpacing: 1 },
  input: { width: '100%', padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: 10, color: '#f1f5f9', fontSize: 15, boxSizing: 'border-box', outline: 'none' },
  roomGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 },
  roomBtn: { padding: '10px 14px', background: '#0f172a', border: '1px solid #334155', borderRadius: 8, color: '#94a3b8', cursor: 'pointer', fontSize: 14, textAlign: 'left', transition: 'all 0.2s' },
  roomBtnActive: { background: '#1e3a5f', border: '1px solid #3b82f6', color: '#60a5fa' },
  primaryBtn: { width: '100%', padding: '14px', background: '#3b82f6', border: 'none', borderRadius: 10, color: 'white', fontSize: 15, fontWeight: 600, cursor: 'pointer', marginTop: 8 },
  hint: { fontSize: 12, color: '#64748b', marginTop: 16, textAlign: 'center' },
  chatLayout: { display: 'flex', height: '100vh' },
  sidebar: { width: 220, background: '#1e293b', borderRight: '1px solid #334155', display: 'flex', flexDirection: 'column' },
  sidebarHeader: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 16px 12px' },
  sidebarTitle: { fontSize: 13, fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase', letterSpacing: 1, margin: 0 },
  addRoomBtn: { width: 24, height: 24, background: '#334155', border: 'none', borderRadius: 6, color: '#94a3b8', cursor: 'pointer', fontSize: 16, lineHeight: 1 },
  createRoomForm: { display: 'flex', gap: 6, padding: '0 12px 12px' },
  createRoomInput: { flex: 1, padding: '6px 10px', background: '#0f172a', border: '1px solid #334155', borderRadius: 6, color: '#f1f5f9', fontSize: 12, outline: 'none' },
  createBtn: { padding: '6px 10px', background: '#3b82f6', border: 'none', borderRadius: 6, color: 'white', fontSize: 12, cursor: 'pointer' },
  roomList: { flex: 1, overflow: 'auto', padding: '0 8px' },
  sidebarRoom: { display: 'block', width: '100%', padding: '8px 12px', background: 'transparent', border: 'none', borderRadius: 6, color: '#94a3b8', cursor: 'pointer', fontSize: 14, textAlign: 'left', marginBottom: 2, transition: 'all 0.15s' },
  sidebarRoomActive: { background: '#334155', color: '#f1f5f9' },
  sidebarFooter: { padding: 16, borderTop: '1px solid #334155', display: 'flex', alignItems: 'center', justifyContent: 'space-between' },
  userInfo: { display: 'flex', alignItems: 'center', gap: 8, fontSize: 13, color: '#94a3b8' },
  userDot: { width: 8, height: 8, background: '#22c55e', borderRadius: '50%' },
  leaveBtn: { padding: '4px 10px', background: 'transparent', border: '1px solid #334155', borderRadius: 6, color: '#94a3b8', cursor: 'pointer', fontSize: 12 },
  chatMain: { flex: 1, display: 'flex', flexDirection: 'column' },
  chatHeader: { display: 'flex', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid #1e293b', background: '#1e293b' },
  hashIcon: { fontSize: 20, color: '#3b82f6', fontWeight: 700, marginRight: 8 },
  roomTitle: { fontSize: 16, fontWeight: 600, color: '#f1f5f9' },
  messagesArea: { flex: 1, overflow: 'auto', padding: '16px 24px' },
  message: { marginBottom: 16, padding: '10px 14px', background: '#1e293b', borderRadius: 8, maxWidth: '70%' },
  systemMessage: { background: 'transparent', border: '1px solid #334155', maxWidth: '100%', textAlign: 'center', fontSize: 13, color: '#64748b', fontStyle: 'italic' },
  messageHeader: { display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 },
  messageUser: { fontWeight: 600, color: '#60a5fa', fontSize: 14 },
  messageTime: { fontSize: 11, color: '#64748b' },
  messageContent: { fontSize: 14, color: '#e2e8f0', lineHeight: 1.5, wordBreak: 'break-word' },
  inputArea: { display: 'flex', gap: 12, padding: '16px 24px', background: '#1e293b', borderTop: '1px solid #334155' },
  chatInput: { flex: 1, padding: '12px 16px', background: '#0f172a', border: '1px solid #334155', borderRadius: 10, color: '#f1f5f9', fontSize: 14, outline: 'none' },
  sendBtn: { padding: '12px 24px', background: '#3b82f6', border: 'none', borderRadius: 10, color: 'white', fontSize: 14, fontWeight: 600, cursor: 'pointer' },
};
