import React, { useState, useEffect, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

const API_URL = 'http://localhost:5002';
const socket: Socket = io(API_URL, { transports: ['websocket', 'polling'] });

interface Option {
  id: number;
  poll_id: string;
  text: string;
  votes: number;
}

interface Poll {
  id: string;
  question: string;
  options: Option[];
  total_votes: number;
  is_active: number;
  created_at: string;
}

export default function App() {
  const [polls, setPolls] = useState<Poll[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [question, setQuestion] = useState('');
  const [options, setOptions] = useState(['', '']);
  const [selectedPoll, setSelectedPoll] = useState<Poll | null>(null);
  const [voted, setVoted] = useState<Record<string, number>>({});
  const [voterId] = useState(() => 'voter_' + Math.random().toString(36).slice(2, 10));

  const loadPolls = useCallback(() => {
    fetch(`${API_URL}/api/polls`)
      .then(r => r.json())
      .then(d => { if (d.success) setPolls(d.data); })
      .catch(() => {});
  }, []);

  useEffect(() => {
    loadPolls();
    socket.on('connect', () => {});
    socket.on('poll_created', (poll: Poll) => {
      setPolls(prev => [poll, ...prev]);
    });
    socket.on('poll_updated', (poll: Poll) => {
      setPolls(prev => prev.map(p => p.id === poll.id ? poll : p));
      if (selectedPoll?.id === poll.id) setSelectedPoll(poll);
    });
    socket.on('poll_closed', (poll: Poll) => {
      setPolls(prev => prev.map(p => p.id === poll.id ? poll : p));
      if (selectedPoll?.id === poll.id) setSelectedPoll(poll);
    });
    return () => {
      socket.off('poll_created');
      socket.off('poll_updated');
      socket.off('poll_closed');
    };
  }, [loadPolls, selectedPoll?.id]);

  const addOption = () => {
    if (options.length < 8) setOptions([...options, '']);
  };

  const removeOption = (i: number) => {
    if (options.length > 2) setOptions(options.filter((_, idx) => idx !== i));
  };

  const updateOption = (i: number, val: string) => {
    const next = [...options];
    next[i] = val;
    setOptions(next);
  };

  const createPoll = () => {
    const validOpts = options.filter(o => o.trim());
    if (!question.trim() || validOpts.length < 2) return;
    fetch(`${API_URL}/api/polls`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: question.trim(), options: validOpts }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setQuestion('');
          setOptions(['', '']);
          setShowCreate(false);
        }
      })
      .catch(() => {});
  };

  const vote = (pollId: string, optionId: number) => {
    if (voted[pollId] !== undefined) return;
    fetch(`${API_URL}/api/polls/${pollId}/vote`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ option_id: optionId, voter_id: voterId }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setVoted(prev => ({ ...prev, [pollId]: optionId }));
          setPolls(prev => prev.map(p => p.id === pollId ? d.data : p));
          if (selectedPoll?.id === pollId) setSelectedPoll(d.data);
        }
      })
      .catch(() => {});
  };

  const closePoll = (pollId: string) => {
    fetch(`${API_URL}/api/polls/${pollId}/close`, { method: 'POST' })
      .then(r => r.json())
      .then(d => { if (d.success) loadPolls(); })
      .catch(() => {});
  };

  const getPercent = (votes: number, total: number) => {
    if (total === 0) return 0;
    return Math.round((votes / total) * 100);
  };

  const getWinningIndex = (poll: Poll) => {
    if (poll.total_votes === 0) return -1;
    let maxVotes = -1, winnerIdx = -1;
    poll.options.forEach((o, i) => { if (o.votes > maxVotes) { maxVotes = o.votes; winnerIdx = i; } });
    return winnerIdx;
  };

  return (
    <div style={styles.container}>
      <div style={styles.layout}>
        <div style={styles.sidebar}>
          <div style={styles.sidebarHeader}>
            <h1 style={styles.logo}>&#128280; Polls</h1>
            <p style={styles.tagline}>Live voting, real-time results</p>
          </div>
          <button style={styles.createBtn} onClick={() => setShowCreate(!showCreate)}>
            + New Poll
          </button>
          <div style={styles.pollList}>
            {polls.map(poll => (
              <button
                key={poll.id}
                style={{ ...styles.pollCard, ...(selectedPoll?.id === poll.id ? styles.pollCardActive : {}) }}
                onClick={() => { setSelectedPoll(poll); socket.emit('join_poll', { poll_id: poll.id }); }}
              >
                <div style={styles.pollQuestion}>{poll.question}</div>
                <div style={styles.pollMeta}>
                  <span style={{ ...styles.badge, background: poll.is_active ? '#166534' : '#6b21a8', color: 'white' }}>
                    {poll.is_active ? 'Active' : 'Closed'}
                  </span>
                  <span style={styles.voteCount}>{poll.total_votes} votes</span>
                </div>
              </button>
            ))}
            {polls.length === 0 && (
              <p style={{ color: '#64748b', fontSize: 14, padding: 20, textAlign: 'center' }}>No polls yet. Create one!</p>
            )}
          </div>
        </div>
        <div style={styles.main}>
          {showCreate && (
            <div style={styles.createPanel}>
              <h2 style={styles.panelTitle}>Create New Poll</h2>
              <div style={styles.formGroup}>
                <label style={styles.label}>Question</label>
                <input style={styles.input} type="text" placeholder="What would you like to ask?" value={question} onChange={e => setQuestion(e.target.value)} maxLength={200} />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>Options</label>
                {options.map((opt, i) => (
                  <div key={i} style={styles.optionRow}>
                    <input style={styles.optionInput} type="text" placeholder={`Option ${i + 1}`} value={opt} onChange={e => updateOption(i, e.target.value)} />
                    {options.length > 2 && <button style={styles.removeBtn} onClick={() => removeOption(i)}>x</button>}
                  </div>
                ))}
                {options.length < 8 && (
                  <button style={styles.addOptBtn} onClick={addOption}>+ Add Option</button>
                )}
              </div>
              <button style={styles.submitBtn} onClick={createPoll} disabled={!question.trim() || options.filter(o => o.trim()).length < 2}>
                Create Poll
              </button>
            </div>
          )}
          {selectedPoll && !showCreate && (
            <div style={styles.pollDetail}>
              <div style={styles.detailHeader}>
                <h2 style={styles.detailQuestion}>{selectedPoll.question}</h2>
                <span style={{ ...styles.badge, background: selectedPoll.is_active ? '#166534' : '#6b21a8', color: 'white' }}>
                  {selectedPoll.is_active ? 'Active' : 'Closed'}
                </span>
              </div>
              <p style={styles.detailMeta}>{selectedPoll.total_votes} total votes</p>
              <div style={styles.optionsList}>
                {selectedPoll.options.map((opt, i) => {
                  const percent = getPercent(opt.votes, selectedPoll.total_votes);
                  const isWinner = !selectedPoll.is_active && i === getWinningIndex(selectedPoll);
                  const isVoted = voted[selectedPoll.id] === opt.id;
                  return (
                    <div key={opt.id} style={styles.optionItem}>
                      <div style={styles.optionTop}>
                        <span style={styles.optionText}>{opt.text}</span>
                        {isVoted && <span style={styles.votedMark}>&#10003; Your vote</span>}
                        {isWinner && <span style={styles.winnerMark}>&#127942;</span>}
                      </div>
                      <div style={styles.barBg}>
                        <div style={{ ...styles.barFill, width: `${percent}%`, background: isWinner ? '#f59e0b' : isVoted ? '#3b82f6' : '#6366f1' }} />
                      </div>
                      <div style={styles.optionBottom}>
                        <span style={styles.optionVotes}>{opt.votes} votes</span>
                        <span style={styles.optionPercent}>{percent}%</span>
                      </div>
                      {selectedPoll.is_active && voted[selectedPoll.id] === undefined && (
                        <button style={styles.voteBtn} onClick={() => vote(selectedPoll.id, opt.id)}>
                          Vote
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
              {selectedPoll.is_active && (
                <button style={styles.closeBtn} onClick={() => closePoll(selectedPoll.id)}>
                  Close Poll
                </button>
              )}
            </div>
          )}
          {!selectedPoll && !showCreate && (
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>&#128280;</div>
              <h2 style={styles.emptyTitle}>Select a Poll</h2>
              <p style={styles.emptyText}>Choose a poll from the sidebar or create a new one</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', background: '#f8fafc', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' },
  layout: { display: 'flex', minHeight: '100vh' },
  sidebar: { width: 320, background: 'white', borderRight: '1px solid #e2e8f0', display: 'flex', flexDirection: 'column' },
  sidebarHeader: { padding: '28px 24px 20px', borderBottom: '1px solid #e2e8f0' },
  logo: { fontSize: 24, fontWeight: 800, color: '#0f172a', margin: 0 },
  tagline: { fontSize: 13, color: '#64748b', marginTop: 4 },
  createBtn: { margin: 16, padding: '10px 16px', background: '#6366f1', border: 'none', borderRadius: 10, color: 'white', fontSize: 14, fontWeight: 600, cursor: 'pointer' },
  pollList: { flex: 1, overflow: 'auto', padding: '0 12px 16px' },
  pollCard: { display: 'block', width: '100%', padding: '14px 16px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, cursor: 'pointer', marginBottom: 8, textAlign: 'left', transition: 'all 0.15s' },
  pollCardActive: { background: '#eef2ff', border: '1px solid #6366f1' },
  pollQuestion: { fontSize: 14, fontWeight: 600, color: '#0f172a', marginBottom: 8 },
  pollMeta: { display: 'flex', alignItems: 'center', gap: 10 },
  badge: { fontSize: 11, padding: '2px 8px', borderRadius: 12, fontWeight: 600 },
  voteCount: { fontSize: 12, color: '#64748b' },
  main: { flex: 1, padding: 32, overflow: 'auto' },
  createPanel: { maxWidth: 560, margin: '0 auto', background: 'white', borderRadius: 16, padding: 32, boxShadow: '0 4px 6px rgba(0,0,0,0.05)' },
  panelTitle: { fontSize: 22, fontWeight: 700, color: '#0f172a', marginBottom: 24 },
  formGroup: { marginBottom: 20 },
  label: { display: 'block', fontSize: 13, fontWeight: 600, color: '#475569', marginBottom: 8 },
  input: { width: '100%', padding: '12px 16px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, fontSize: 15, color: '#0f172a', boxSizing: 'border-box', outline: 'none' },
  optionRow: { display: 'flex', gap: 8, marginBottom: 8 },
  optionInput: { flex: 1, padding: '10px 14px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 8, fontSize: 14, color: '#0f172a', outline: 'none' },
  removeBtn: { width: 32, height: 32, background: '#fee2e2', border: 'none', borderRadius: 8, color: '#ef4444', cursor: 'pointer', fontSize: 16 },
  addOptBtn: { padding: '8px 14px', background: 'transparent', border: '1px dashed #cbd5e1', borderRadius: 8, color: '#64748b', cursor: 'pointer', fontSize: 13, marginTop: 4 },
  submitBtn: { width: '100%', padding: '14px', background: '#6366f1', border: 'none', borderRadius: 10, color: 'white', fontSize: 15, fontWeight: 600, cursor: 'pointer', marginTop: 8 },
  pollDetail: { maxWidth: 640, margin: '0 auto', background: 'white', borderRadius: 16, padding: 32, boxShadow: '0 4px 6px rgba(0,0,0,0.05)' },
  detailHeader: { display: 'flex', alignItems: 'center', gap: 16, marginBottom: 8 },
  detailQuestion: { fontSize: 22, fontWeight: 700, color: '#0f172a', margin: 0 },
  detailMeta: { fontSize: 14, color: '#64748b', marginBottom: 24 },
  optionsList: { display: 'flex', flexDirection: 'column', gap: 16 },
  optionItem: { padding: 16, background: '#f8fafc', borderRadius: 12, border: '1px solid #e2e8f0', position: 'relative' },
  optionTop: { display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 },
  optionText: { fontSize: 15, fontWeight: 600, color: '#0f172a' },
  votedMark: { fontSize: 12, color: '#3b82f6', fontWeight: 600 },
  winnerMark: { fontSize: 16 },
  barBg: { height: 8, background: '#e2e8f0', borderRadius: 4, overflow: 'hidden' },
  barFill: { height: '100%', borderRadius: 4, transition: 'width 0.5s ease' },
  optionBottom: { display: 'flex', justifyContent: 'space-between', marginTop: 6, fontSize: 13, color: '#64748b' },
  optionVotes: {},
  optionPercent: { fontWeight: 700, color: '#0f172a' },
  voteBtn: { position: 'absolute', top: 16, right: 16, padding: '6px 16px', background: '#6366f1', border: 'none', borderRadius: 8, color: 'white', fontSize: 13, fontWeight: 600, cursor: 'pointer' },
  closeBtn: { marginTop: 24, padding: '12px 24px', background: '#6b21a8', border: 'none', borderRadius: 10, color: 'white', fontSize: 14, fontWeight: 600, cursor: 'pointer' },
  emptyState: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', color: '#94a3b8' },
  emptyIcon: { fontSize: 64, marginBottom: 16 },
  emptyTitle: { fontSize: 22, fontWeight: 700, color: '#64748b', margin: 0 },
  emptyText: { fontSize: 14, color: '#94a3b8' },
};
