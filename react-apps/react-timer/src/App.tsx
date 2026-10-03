import { useState, useEffect, useCallback } from 'react';

const PRESETS = [
  { label: '1 min', seconds: 60 },
  { label: '5 min', seconds: 300 },
  { label: '10 min', seconds: 600 },
  { label: '15 min', seconds: 900 },
  { label: '30 min', seconds: 1800 },
  { label: '60 min', seconds: 3600 },
];

function formatTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

export default function App() {
  const [selectedSeconds, setSelectedSeconds] = useState<number>(300);
  const [timeLeft, setTimeLeft] = useState<number>(300);
  const [isRunning, setIsRunning] = useState<boolean>(false);

  const requestNotification = useCallback(() => {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification('Timer Complete!', { body: 'Your countdown has finished.', badge: undefined });
    }
  }, []);

  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  useEffect(() => {
    if (!isRunning || timeLeft <= 0) return;
    const id = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          setIsRunning(false);
          requestNotification();
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(id);
  }, [isRunning, timeLeft, requestNotification]);

  const start = () => setIsRunning(true);
  const pause = () => setIsRunning(false);
  const reset = () => {
    setIsRunning(false);
    setTimeLeft(selectedSeconds);
  };

  const selectPreset = (seconds: number) => {
    setSelectedSeconds(seconds);
    setTimeLeft(seconds);
    setIsRunning(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Countdown Timer</h1>
        <div style={styles.display}>{formatTime(timeLeft)}</div>
        <div style={styles.controls}>
          {!isRunning ? (
            <button style={styles.btn} onClick={start}>Start</button>
          ) : (
            <button style={styles.btn} onClick={pause}>Pause</button>
          )}
          <button style={{ ...styles.btn, ...styles.btnSecondary }} onClick={reset}>Reset</button>
        </div>
        <div style={styles.presets}>
          {PRESETS.map((p) => (
            <button
              key={p.seconds}
              style={{
                ...styles.presetBtn,
                ...(selectedSeconds === p.seconds ? styles.presetBtnActive : {}),
              }}
              onClick={() => selectPreset(p.seconds)}
            >
              {p.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    background: '#0f0f0f',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'system-ui, sans-serif',
    color: '#fff',
  },
  card: {
    background: '#1a1a1a',
    borderRadius: 16,
    padding: 40,
    textAlign: 'center',
    boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
    minWidth: 340,
  },
  title: { fontSize: 24, fontWeight: 600, marginBottom: 24, color: '#e0e0e0' },
  display: {
    fontSize: 64,
    fontWeight: 700,
    fontVariantNumeric: 'tabular-nums',
    letterSpacing: 4,
    marginBottom: 32,
    color: '#00d4ff',
    textShadow: '0 0 20px rgba(0,212,255,0.3)',
  },
  controls: { display: 'flex', gap: 12, justifyContent: 'center', marginBottom: 28 },
  btn: {
    padding: '12px 32px',
    fontSize: 16,
    fontWeight: 600,
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    background: '#00d4ff',
    color: '#0f0f0f',
    transition: 'opacity 0.2s',
  },
  btnSecondary: { background: '#333', color: '#fff' },
  presets: { display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center' },
  presetBtn: {
    padding: '8px 16px',
    fontSize: 14,
    border: '1px solid #333',
    borderRadius: 6,
    cursor: 'pointer',
    background: 'transparent',
    color: '#aaa',
    transition: 'all 0.2s',
  },
  presetBtnActive: { borderColor: '#00d4ff', color: '#00d4ff', background: 'rgba(0,212,255,0.1)' },
};
