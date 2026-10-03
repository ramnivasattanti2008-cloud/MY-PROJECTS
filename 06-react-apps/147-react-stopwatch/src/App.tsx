import { useState, useRef, useEffect } from 'react';

interface Lap {
  number: number;
  time: number;
}

export default function App() {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const [laps, setLaps] = useState<Lap[]>([]);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = window.setInterval(() => {
        setTime((t) => t + 10);
      }, 10);
    }
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning]);

  const formatTime = (ms: number) => {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    const centiseconds = Math.floor((ms % 1000) / 10);
    return {
      minutes: String(minutes).padStart(2, '0'),
      seconds: String(seconds).padStart(2, '0'),
      centiseconds: String(centiseconds).padStart(2, '0'),
    };
  };

  const { minutes, seconds, centiseconds } = formatTime(time);

  const handleStart = () => setIsRunning(true);
  const handlePause = () => setIsRunning(false);
  const handleReset = () => {
    setIsRunning(false);
    setTime(0);
    setLaps([]);
  };

  const handleLap = () => {
    setLaps((prev) => [{ number: prev.length + 1, time }, ...prev]);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Stopwatch</h1>

        <div style={styles.display}>
          <span style={styles.digit}>{minutes}</span>
          <span style={styles.separator}>:</span>
          <span style={styles.digit}>{seconds}</span>
          <span style={styles.separator}>.</span>
          <span style={styles.centis}>{centiseconds}</span>
        </div>

        <div style={styles.buttons}>
          {!isRunning ? (
            <button style={styles.startBtn} onClick={handleStart}>
              {time === 0 ? 'Start' : 'Resume'}
            </button>
          ) : (
            <button style={styles.pauseBtn} onClick={handlePause}>
              Pause
            </button>
          )}
          <button style={styles.resetBtn} onClick={handleReset} disabled={time === 0}>
            Reset
          </button>
          <button style={styles.lapBtn} onClick={handleLap} disabled={!isRunning && time === 0}>
            Lap
          </button>
        </div>

        {laps.length > 0 && (
          <div style={styles.lapsContainer}>
            <h2 style={styles.lapsTitle}>Laps ({laps.length})</h2>
            <div style={styles.lapsList}>
              {laps.map((lap) => {
                const lapTime = formatTime(lap.time);
                return (
                  <div key={lap.number} style={styles.lapItem}>
                    <span style={styles.lapNumber}>Lap {lap.number}</span>
                    <span style={styles.lapTime}>
                      {lapTime.minutes}:{lapTime.seconds}.{lapTime.centiseconds}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#0f0f0f',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    padding: '1rem',
  },
  card: {
    backgroundColor: '#1a1a1a',
    borderRadius: '24px',
    padding: '3rem',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
    width: '100%',
    maxWidth: '400px',
  },
  title: {
    color: '#fff',
    fontSize: '1.5rem',
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: '2rem',
  },
  display: {
    display: 'flex',
    alignItems: 'baseline',
    justifyContent: 'center',
    marginBottom: '2.5rem',
  },
  digit: {
    fontSize: '4rem',
    fontWeight: '700',
    color: '#fff',
    fontVariantNumeric: 'tabular-nums',
  },
  separator: {
    fontSize: '4rem',
    fontWeight: '700',
    color: '#666',
    margin: '0 0.25rem',
  },
  centis: {
    fontSize: '2rem',
    fontWeight: '600',
    color: '#888',
    fontVariantNumeric: 'tabular-nums',
  },
  buttons: {
    display: 'flex',
    gap: '0.75rem',
    justifyContent: 'center',
    marginBottom: '2rem',
  },
  startBtn: {
    flex: 1,
    padding: '1rem 1.5rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: 'none',
    backgroundColor: '#22c55e',
    color: '#fff',
    cursor: 'pointer',
    transition: 'transform 0.1s',
  },
  pauseBtn: {
    flex: 1,
    padding: '1rem 1.5rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: 'none',
    backgroundColor: '#f59e0b',
    color: '#fff',
    cursor: 'pointer',
  },
  resetBtn: {
    flex: 1,
    padding: '1rem 1.5rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: '1px solid #333',
    backgroundColor: 'transparent',
    color: '#999',
    cursor: 'pointer',
  },
  lapBtn: {
    flex: 1,
    padding: '1rem 1.5rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: '1px solid #333',
    backgroundColor: 'transparent',
    color: '#999',
    cursor: 'pointer',
  },
  lapsContainer: {
    borderTop: '1px solid #333',
    paddingTop: '1.5rem',
  },
  lapsTitle: {
    color: '#fff',
    fontSize: '1rem',
    fontWeight: '600',
    marginBottom: '1rem',
  },
  lapsList: {
    maxHeight: '200px',
    overflowY: 'auto',
  },
  lapItem: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '0.75rem 0',
    borderBottom: '1px solid #222',
  },
  lapNumber: {
    color: '#888',
    fontSize: '0.875rem',
  },
  lapTime: {
    color: '#fff',
    fontSize: '0.875rem',
    fontWeight: '600',
    fontVariantNumeric: 'tabular-nums',
  },
};
