import { useState, useRef } from 'react';

const MEME_TEMPLATES = [
  { url: 'https://i.imgflip.com/1bij.jpg', name: 'One Does Not Simply' },
  { url: 'https://i.imgflip.com/9ehk.jpg', name: 'Bad Luck Brian' },
  { url: 'https://i.imgflip.com/1bhw.jpg', name: 'Y U No' },
  { url: 'https://i.imgflip.com/1ur9b0.jpg', name: 'Distracted Boyfriend' },
  { url: 'https://i.imgflip.com/30b1gx.jpg', name: 'Woman Yelling at Cat' },
];

export default function App() {
  const [template, setTemplate] = useState(MEME_TEMPLATES[0].url);
  const [topText, setTopText] = useState('');
  const [bottomText, setBottomText] = useState('');
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const downloadMeme = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      const fontSize = Math.floor(img.width / 8);
      ctx.font = `bold ${fontSize}px Impact, sans-serif`;
      ctx.textAlign = 'center';
      ctx.fillStyle = '#fff';
      ctx.strokeStyle = '#000';
      ctx.lineWidth = fontSize / 15;

      const x = img.width / 2;
      const topY = fontSize * 1.2;
      const bottomY = img.height - fontSize / 4;

      const wrapText = (text: string, maxWidth: number) => {
        const words = text.split(' ');
        const lines: string[] = [];
        let line = '';
        for (const word of words) {
          const test = line ? `${line} ${word}` : word;
          if (ctx.measureText(test).width > maxWidth && line) {
            lines.push(line);
            line = word;
          } else {
            line = test;
          }
        }
        if (line) lines.push(line);
        return lines;
      };

      const maxWidth = img.width * 0.9;

      // Top text
      const topLines = wrapText(topText, maxWidth);
      let y = topY;
      for (const line of topLines) {
        ctx.strokeText(line, x, y);
        ctx.fillText(line, x, y);
        y += fontSize * 1.1;
      }

      // Bottom text
      const bottomLines = wrapText(bottomText, maxWidth);
      y = bottomY - (bottomLines.length - 1) * fontSize * 1.1;
      for (const line of bottomLines) {
        ctx.strokeText(line, x, y);
        ctx.fillText(line, x, y);
        y += fontSize * 1.1;
      }

      const a = document.createElement('a');
      a.href = canvas.toDataURL('image/png');
      a.download = 'meme.png';
      a.click();
    };
    img.src = template;
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Meme Generator</h1>
        <div style={styles.select}>
          {MEME_TEMPLATES.map((t) => (
            <button
              key={t.url}
              style={{ ...styles.templateBtn, ...(template === t.url ? styles.templateBtnActive : {}) }}
              onClick={() => setTemplate(t.url)}
            >
              {t.name}
            </button>
          ))}
        </div>
        <div style={styles.preview}>
          <div style={styles.memeContainer}>
            <img src={template} alt="Meme template" style={styles.memeImg} />
            <div style={styles.topText}>{topText}</div>
            <div style={styles.bottomText}>{bottomText}</div>
          </div>
        </div>
        <div style={styles.inputs}>
          <input
            style={styles.input}
            placeholder="TOP TEXT"
            value={topText}
            onChange={(e) => setTopText(e.target.value.toUpperCase())}
          />
          <input
            style={styles.input}
            placeholder="BOTTOM TEXT"
            value={bottomText}
            onChange={(e) => setBottomText(e.target.value.toUpperCase())}
          />
        </div>
        <button style={styles.downloadBtn} onClick={downloadMeme}>
          Download Meme
        </button>
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
    padding: 24,
  },
  card: {
    background: '#1a1a1a',
    borderRadius: 16,
    padding: 32,
    textAlign: 'center',
    boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
    width: '100%',
    maxWidth: 540,
  },
  title: { fontSize: 24, fontWeight: 700, marginBottom: 20, color: '#e0e0e0' },
  select: { display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: 'center', marginBottom: 20 },
  templateBtn: {
    padding: '6px 12px',
    fontSize: 12,
    border: '1px solid #333',
    borderRadius: 6,
    cursor: 'pointer',
    background: 'transparent',
    color: '#888',
    transition: 'all 0.15s',
  },
  templateBtnActive: { borderColor: '#f97316', color: '#f97316', background: 'rgba(249,115,22,0.1)' },
  preview: { marginBottom: 20 },
  memeContainer: { position: 'relative', display: 'inline-block' },
  memeImg: { maxWidth: '100%', borderRadius: 8, display: 'block' },
  topText: {
    position: 'absolute',
    top: 16,
    left: '50%',
    transform: 'translateX(-50%)',
    fontSize: 28,
    fontWeight: 900,
    fontFamily: 'Impact, sans-serif',
    color: '#fff',
    textShadow: '3px 3px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000',
    width: '90%',
    textAlign: 'center',
    pointerEvents: 'none',
  },
  bottomText: {
    position: 'absolute',
    bottom: 16,
    left: '50%',
    transform: 'translateX(-50%)',
    fontSize: 28,
    fontWeight: 900,
    fontFamily: 'Impact, sans-serif',
    color: '#fff',
    textShadow: '3px 3px 0 #000, -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000',
    width: '90%',
    textAlign: 'center',
    pointerEvents: 'none',
  },
  inputs: { display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 20 },
  input: {
    padding: '12px 16px',
    fontSize: 16,
    fontWeight: 700,
    textTransform: 'uppercase',
    border: '1px solid #333',
    borderRadius: 8,
    background: '#0f0f0f',
    color: '#fff',
    outline: 'none',
    textAlign: 'center',
    letterSpacing: 1,
  },
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
