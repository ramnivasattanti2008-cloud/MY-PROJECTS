import { useState, useEffect, useRef } from 'react';
import QRCode from 'qrcode';

export default function App() {
  const [text, setText] = useState('https://example.com');
  const [qrDataUrl, setQrDataUrl] = useState('');
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!text.trim()) {
      setQrDataUrl('');
      return;
    }
    QRCode.toDataURL(text, { width: 300, margin: 2, color: { dark: '#ffffff', light: '#00000000' } })
      .then(setQrDataUrl)
      .catch(() => setQrDataUrl(''));
  }, [text]);

  const download = () => {
    if (!qrDataUrl) return;
    const a = document.createElement('a');
    a.href = qrDataUrl;
    a.download = 'qrcode.png';
    a.click();
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>QR Code Generator</h1>
        <div style={styles.inputGroup}>
          <input
            style={styles.input}
            placeholder="Enter text or URL..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>
        <div style={styles.preview}>
          {qrDataUrl ? (
            <img src={qrDataUrl} alt="QR Code" style={styles.qrImage} />
          ) : (
            <div style={styles.placeholder}>Enter text above to generate</div>
          )}
        </div>
        {qrDataUrl && (
          <button style={styles.downloadBtn} onClick={download}>
            Download PNG
          </button>
        )}
      </div>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
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
    padding: 16,
  },
  card: {
    background: '#1a1a1a',
    borderRadius: 16,
    padding: 40,
    textAlign: 'center',
    boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
    width: '100%',
    maxWidth: 400,
  },
  title: { fontSize: 24, fontWeight: 700, marginBottom: 24, color: '#e0e0e0' },
  inputGroup: { marginBottom: 24 },
  input: {
    width: '100%',
    padding: '12px 16px',
    fontSize: 16,
    border: '1px solid #333',
    borderRadius: 8,
    background: '#0f0f0f',
    color: '#fff',
    outline: 'none',
    boxSizing: 'border-box',
  },
  preview: {
    marginBottom: 24,
    minHeight: 300,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  qrImage: { width: 280, height: 280, borderRadius: 8 },
  placeholder: { color: '#444', fontSize: 16 },
  downloadBtn: {
    padding: '14px 32px',
    fontSize: 16,
    fontWeight: 600,
    border: 'none',
    borderRadius: 8,
    cursor: 'pointer',
    background: '#f97316',
    color: '#fff',
  },
};
