import React, { useState, useEffect, useCallback } from 'react';

const API_URL = 'http://localhost:5004';

interface Paste {
  id: string;
  title: string;
  language: string;
  created_at: string;
  view_count: number;
}

interface PasteDetail {
  id: string;
  title: string;
  language: string;
  code: string;
  highlighted_html?: string;
  created_at: string;
  view_count: number;
}

const LANGUAGES = [
  'javascript', 'typescript', 'python', 'java', 'cpp', 'c', 'csharp', 'go',
  'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'html', 'css', 'sql',
  'bash', 'powershell', 'json', 'yaml', 'xml', 'markdown', 'text',
];

export default function App() {
  const [view, setView] = useState<'create' | 'recent' | 'paste'>('create');
  const [pastes, setPastes] = useState<Paste[]>([]);
  const [selectedPaste, setSelectedPaste] = useState<PasteDetail | null>(null);
  const [title, setTitle] = useState('');
  const [language, setLanguage] = useState('javascript');
  const [code, setCode] = useState('');
  const [shareUrl, setShareUrl] = useState('');
  const [copyFeedback, setCopyFeedback] = useState(false);

  const loadPastes = useCallback(() => {
    fetch(`${API_URL}/api/pastes`)
      .then(r => r.json())
      .then(d => { if (d.success) setPastes(d.data); })
      .catch(() => {});
  }, []);

  useEffect(() => { loadPastes(); }, [loadPastes]);

  const createPaste = () => {
    if (!code.trim()) return;
    fetch(`${API_URL}/api/pastes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, language, title: title || 'Untitled' }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setShareUrl(`http://localhost:5004${d.data.url}`);
          loadPastes();
        }
      })
      .catch(() => {});
  };

  const viewPaste = (pasteId: string) => {
    fetch(`${API_URL}/api/pastes/${pasteId}`)
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setSelectedPaste(d.data);
          setView('paste');
        }
      })
      .catch(() => {});
  };

  const copyToClipboard = () => {
    if (!selectedPaste) return;
    navigator.clipboard.writeText(selectedPaste.code).then(() => {
      setCopyFeedback(true);
      setTimeout(() => setCopyFeedback(false), 2000);
    });
  };

  const formatDate = (ts: string) => {
    try { return new Date(ts).toLocaleDateString(); } catch { return ts; }
  };

  return (
    <div style={styles.container}>
      <div style={styles.topBar}>
        <h1 style={styles.logo}>&lt;/&gt; CodePaste</h1>
        <div style={styles.tabs}>
          <button style={{ ...styles.tab, ...(view === 'create' ? styles.tabActive : {}) }} onClick={() => setView('create')}>New Paste</button>
          <button style={{ ...styles.tab, ...(view === 'recent' ? styles.tabActive : {}) }} onClick={() => { loadPastes(); setView('recent'); }}>Recent</button>
        </div>
      </div>
      <div style={styles.main}>
        {view === 'create' && (
          <div style={styles.createView}>
            <div style={styles.formRow}>
              <input
                style={styles.titleInput}
                type="text"
                placeholder="Paste title (optional)"
                value={title}
                onChange={e => setTitle(e.target.value)}
              />
              <select style={styles.langSelect} value={language} onChange={e => setLanguage(e.target.value)}>
                {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
              </select>
            </div>
            <textarea
              style={styles.codeEditor}
              placeholder="Paste your code here..."
              value={code}
              onChange={e => setCode(e.target.value)}
              spellCheck={false}
            />
            <div style={styles.formFooter}>
              <span style={styles.lineCount}>{code.split('\n').length} lines</span>
              <button style={{ ...styles.createBtn, ...(code.trim() ? {} : styles.createBtnDisabled) }} onClick={createPaste} disabled={!code.trim()}>
                Create Paste
              </button>
            </div>
            {shareUrl && (
              <div style={styles.shareBox}>
                <p style={styles.shareLabel}>Paste created!</p>
                <div style={styles.shareRow}>
                  <input style={styles.shareInput} type="text" readOnly value={shareUrl} />
                  <button style={styles.copyBtn} onClick={() => { navigator.clipboard.writeText(shareUrl); }}>Copy</button>
                </div>
              </div>
            )}
          </div>
        )}
        {view === 'recent' && (
          <div style={styles.recentView}>
            <h2 style={styles.sectionTitle}>Recent Pastes</h2>
            <div style={styles.pasteGrid}>
              {pastes.map(paste => (
                <div key={paste.id} style={styles.pasteCard} onClick={() => viewPaste(paste.id)}>
                  <div style={styles.cardHeader}>
                    <span style={styles.cardLang}>{paste.language}</span>
                    <span style={styles.cardViews}>{paste.view_count} views</span>
                  </div>
                  <h3 style={styles.cardTitle}>{paste.title}</h3>
                  <p style={styles.cardDate}>{formatDate(paste.created_at)}</p>
                </div>
              ))}
            </div>
            {pastes.length === 0 && <p style={styles.empty}>No pastes yet. Create your first one!</p>}
          </div>
        )}
        {view === 'paste' && selectedPaste && (
          <div style={styles.pasteView}>
            <button style={styles.backBtn} onClick={() => setView('recent')}>&larr; Back</button>
            <div style={styles.pasteHeader}>
              <h2 style={styles.pasteTitle}>{selectedPaste.title}</h2>
              <div style={styles.pasteMeta}>
                <span style={styles.metaBadge}>{selectedPaste.language}</span>
                <span style={styles.metaText}>{formatDate(selectedPaste.created_at)}</span>
                <span style={styles.metaText}>{selectedPaste.view_count} views</span>
              </div>
            </div>
            <div style={styles.toolbar}>
              <button style={styles.toolBtn} onClick={copyToClipboard}>{copyFeedback ? 'Copied!' : 'Copy Code'}</button>
              <button style={styles.toolBtn} onClick={() => window.open(`${API_URL}/api/pastes/${selectedPaste.id}/raw`)}>Download</button>
            </div>
            <pre style={styles.codeBlock}>
              <code>{selectedPaste.code}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', background: '#0d1117', color: '#e6edf3', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", monospace' },
  topBar: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 32px', borderBottom: '1px solid #21262d' },
  logo: { fontSize: 22, fontWeight: 800, color: '#58a6ff', margin: 0 },
  tabs: { display: 'flex', gap: 4 },
  tab: { padding: '8px 20px', background: 'transparent', border: '1px solid #30363d', borderRadius: 8, color: '#8b949e', cursor: 'pointer', fontSize: 14 },
  tabActive: { background: '#1f6feb', border: '1px solid #1f6feb', color: 'white' },
  main: { maxWidth: 1100, margin: '0 auto', padding: 32 },
  createView: {},
  formRow: { display: 'flex', gap: 12, marginBottom: 16 },
  titleInput: { flex: 1, padding: '12px 16px', background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 15, outline: 'none' },
  langSelect: { padding: '12px 16px', background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14, cursor: 'pointer' },
  codeEditor: { width: '100%', minHeight: 400, padding: 16, background: '#161b22', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', fontSize: 14, fontFamily: '"Fira Code", "Cascadia Code", "JetBrains Mono", monospace', resize: 'vertical', outline: 'none', lineHeight: 1.6, boxSizing: 'border-box' },
  formFooter: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 16 },
  lineCount: { fontSize: 13, color: '#8b949e' },
  createBtn: { padding: '12px 28px', background: '#238636', border: 'none', borderRadius: 8, color: 'white', fontSize: 15, fontWeight: 600, cursor: 'pointer' },
  createBtnDisabled: { background: '#1a4d2e', color: '#6e7681', cursor: 'not-allowed' },
  shareBox: { marginTop: 20, padding: 20, background: '#161b22', border: '1px solid #30363d', borderRadius: 8 },
  shareLabel: { fontSize: 14, color: '#3fb950', marginBottom: 10 },
  shareRow: { display: 'flex', gap: 8 },
  shareInput: { flex: 1, padding: '10px 14px', background: '#0d1117', border: '1px solid #30363d', borderRadius: 6, color: '#58a6ff', fontSize: 13 },
  copyBtn: { padding: '10px 20px', background: '#1f6feb', border: 'none', borderRadius: 6, color: 'white', fontSize: 14, cursor: 'pointer' },
  recentView: {},
  sectionTitle: { fontSize: 20, fontWeight: 700, color: '#e6edf3', marginBottom: 20 },
  pasteGrid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 16 },
  pasteCard: { padding: 20, background: '#161b22', border: '1px solid #30363d', borderRadius: 10, cursor: 'pointer', transition: 'all 0.15s' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', marginBottom: 10 },
  cardLang: { fontSize: 12, padding: '2px 8px', background: '#1f6feb', borderRadius: 12, color: 'white', fontWeight: 600 },
  cardViews: { fontSize: 12, color: '#8b949e' },
  cardTitle: { fontSize: 16, fontWeight: 600, color: '#e6edf3', margin: '0 0 8px' },
  cardDate: { fontSize: 12, color: '#8b949e', margin: 0 },
  empty: { textAlign: 'center', padding: 60, color: '#8b949e' },
  pasteView: {},
  backBtn: { padding: '8px 16px', background: 'transparent', border: '1px solid #30363d', borderRadius: 8, color: '#8b949e', cursor: 'pointer', marginBottom: 20, fontSize: 14 },
  pasteHeader: { marginBottom: 16 },
  pasteTitle: { fontSize: 24, fontWeight: 700, color: '#e6edf3', margin: '0 0 12px' },
  pasteMeta: { display: 'flex', alignItems: 'center', gap: 16 },
  metaBadge: { fontSize: 12, padding: '2px 10px', background: '#1f6feb', borderRadius: 12, color: 'white', fontWeight: 600 },
  metaText: { fontSize: 13, color: '#8b949e' },
  toolbar: { display: 'flex', gap: 10, marginBottom: 16 },
  toolBtn: { padding: '8px 16px', background: '#21262d', border: '1px solid #30363d', borderRadius: 8, color: '#e6edf3', cursor: 'pointer', fontSize: 13 },
  codeBlock: { background: '#161b22', border: '1px solid #30363d', borderRadius: 10, padding: 20, overflow: 'auto', fontSize: 14, lineHeight: 1.6, maxHeight: '70vh', margin: 0 },
};
