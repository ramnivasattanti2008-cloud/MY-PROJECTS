import React, { useState, useEffect, useCallback } from 'react';

const API_URL = 'http://localhost:5005';

interface Link {
  id: number;
  url: string;
  title: string;
  description: string;
  tags: string;
  is_favorite: number;
  visit_count: number;
  created_at: string;
}

interface Tag {
  name: string;
  count: number;
}

interface Stats {
  total: number;
  favorites: number;
  total_visits: number;
  tag_count: number;
}

export default function App() {
  const [links, setLinks] = useState<Link[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [stats, setStats] = useState<Stats>({ total: 0, favorites: 0, total_visits: 0, tag_count: 0 });
  const [showAdd, setShowAdd] = useState(false);
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tagInput, setTagInput] = useState('');
  const [search, setSearch] = useState('');
  const [filterTag, setFilterTag] = useState('');
  const [showFavorites, setShowFavorites] = useState(false);
  const [editId, setEditId] = useState<number | null>(null);

  const loadLinks = useCallback(() => {
    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (filterTag) params.set('tag', filterTag);
    if (showFavorites) params.set('favorites', 'true');
    fetch(`${API_URL}/api/links?${params}`)
      .then(r => r.json())
      .then(d => { if (d.success) setLinks(d.data); })
      .catch(() => {});
  }, [search, filterTag, showFavorites]);

  const loadTags = useCallback(() => {
    fetch(`${API_URL}/api/tags`)
      .then(r => r.json())
      .then(d => { if (d.success) setTags(d.data); })
      .catch(() => {});
  }, []);

  const loadStats = useCallback(() => {
    fetch(`${API_URL}/api/stats`)
      .then(r => r.json())
      .then(d => { if (d.success) setStats(d.data); })
      .catch(() => {});
  }, []);

  useEffect(() => { loadLinks(); }, [loadLinks]);
  useEffect(() => { loadTags(); }, [loadTags]);
  useEffect(() => { loadStats(); }, [loadStats]);

  const addLink = () => {
    if (!url.trim()) return;
    const tagList = tagInput.split(',').map(t => t.trim()).filter(Boolean).join(',');
    fetch(`${API_URL}/api/links`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url.trim(), title: title || url, description, tags: tagList }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setUrl(''); setTitle(''); setDescription(''); setTagInput('');
          setShowAdd(false);
          loadLinks(); loadTags(); loadStats();
        }
      })
      .catch(() => {});
  };

  const deleteLink = (id: number) => {
    if (!confirm('Delete this link?')) return;
    fetch(`${API_URL}/api/links/${id}`, { method: 'DELETE' })
      .then(r => r.json())
      .then(d => { if (d.success) { loadLinks(); loadStats(); } })
      .catch(() => {});
  };

  const toggleFavorite = (id: number) => {
    fetch(`${API_URL}/api/links/${id}/favorite`, { method: 'POST' })
      .then(r => r.json())
      .then(() => { loadLinks(); loadStats(); })
      .catch(() => {});
  };

  const visitLink = (id: number, linkUrl: string) => {
    fetch(`${API_URL}/api/links/${id}/visit`, { method: 'POST' })
      .then(() => { loadStats(); window.open(linkUrl, '_blank'); })
      .catch(() => window.open(linkUrl, '_blank'));
  };

  const updateLink = () => {
    if (editId === null) return;
    fetch(`${API_URL}/api/links/${editId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, description, tags: tagInput }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setEditId(null);
          setTitle(''); setDescription(''); setTagInput('');
          loadLinks(); loadTags();
        }
      })
      .catch(() => {});
  };

  const startEdit = (link: Link) => {
    setEditId(link.id);
    setTitle(link.title);
    setDescription(link.description);
    setTagInput(link.tags);
    setShowAdd(true);
  };

  const getDomain = (url: string) => {
    try { return new URL(url).hostname; } catch { return url; }
  };

  const tagColors: Record<string, string> = {
    code: '#f97316', tools: '#22c55e', web: '#3b82f6', python: '#fbbf24',
    javascript: '#facc15', frontend: '#a855f7', docs: '#06b6d4', community: '#ec4899',
  };
  const getTagColor = (tag: string) => tagColors[tag.toLowerCase()] || '#6366f1';

  return (
    <div style={styles.container}>
      <div style={styles.topBar}>
        <h1 style={styles.logo}>&#128279; LinkVault</h1>
        <div style={styles.topActions}>
          <button style={styles.addBtn} onClick={() => { setShowAdd(!showAdd); setEditId(null); setUrl(''); setTitle(''); setDescription(''); setTagInput(''); }}>
            + Add Link
          </button>
        </div>
      </div>
      <div style={styles.layout}>
        <aside style={styles.sidebar}>
          <div style={styles.statsCard}>
            <h3 style={styles.statsTitle}>Collection</h3>
            <div style={styles.statRow}><span style={styles.statNum}>{stats.total}</span><span style={styles.statLabel}>Total Links</span></div>
            <div style={styles.statRow}><span style={styles.statNum}>{stats.favorites}</span><span style={styles.statLabel}>Favorites</span></div>
            <div style={styles.statRow}><span style={styles.statNum}>{stats.total_visits}</span><span style={styles.statLabel}>Total Visits</span></div>
          </div>
          <div style={styles.tagsSection}>
            <h3 style={styles.tagsTitle}>Tags</h3>
            <button style={{ ...styles.tagBtn, ...(filterTag === '' ? styles.tagBtnActive : {}) }} onClick={() => setFilterTag('')}>All</button>
            {tags.map(tag => (
              <button key={tag.name} style={{ ...styles.tagBtn, ...(filterTag === tag.name ? styles.tagBtnActive : {}) }} onClick={() => setFilterTag(filterTag === tag.name ? '' : tag.name)}>
                <span style={{ ...styles.tagDot, background: getTagColor(tag.name) }} />
                {tag.name} <span style={styles.tagCount}>{tag.count}</span>
              </button>
            ))}
          </div>
          <button style={{ ...styles.favBtn, ...(showFavorites ? styles.favBtnActive : {}) }} onClick={() => setShowFavorites(!showFavorites)}>
            &#9733; Favorites
          </button>
        </aside>
        <main style={styles.main}>
          <div style={styles.searchBar}>
            <input
              style={styles.searchInput}
              type="text"
              placeholder="Search links..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          {showAdd && (
            <div style={styles.addForm}>
              <h3 style={styles.formTitle}>{editId ? 'Edit Link' : 'Add New Link'}</h3>
              <input style={styles.urlInput} type="url" placeholder="https://example.com" value={url} onChange={e => setUrl(e.target.value)} />
              <input style={styles.input} type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} />
              <input style={styles.input} type="text" placeholder="Description (optional)" value={description} onChange={e => setDescription(e.target.value)} />
              <input style={styles.input} type="text" placeholder="Tags (comma-separated, e.g. code,python,docs)" value={tagInput} onChange={e => setTagInput(e.target.value)} />
              <div style={styles.formBtns}>
                <button style={styles.cancelBtn} onClick={() => { setShowAdd(false); setEditId(null); }}>Cancel</button>
                <button style={styles.saveBtn} onClick={editId ? updateLink : addLink}>{editId ? 'Update' : 'Save'}</button>
              </div>
            </div>
          )}
          <div style={styles.linkList}>
            {links.map(link => (
              <div key={link.id} style={styles.linkCard}>
                <div style={styles.linkMain} onClick={() => visitLink(link.id, link.url)}>
                  <div style={styles.linkTitle}>{link.title}</div>
                  <div style={styles.linkUrl}>{getDomain(link.url)}</div>
                  {link.description && <div style={styles.linkDesc}>{link.description}</div>}
                  <div style={styles.linkTags}>
                    {link.tags.split(',').filter(Boolean).map((tag, i) => (
                      <span key={i} style={{ ...styles.tagPill, background: getTagColor(tag) + '22', color: getTagColor(tag), border: `1px solid ${getTagColor(tag)}44` }}>{tag}</span>
                    ))}
                  </div>
                </div>
                <div style={styles.linkActions}>
                  <button style={styles.iconBtn} onClick={() => toggleFavorite(link.id)} title="Toggle favorite">
                    {link.is_favorite ? '★' : '☆'}
                  </button>
                  <button style={styles.iconBtn} onClick={() => startEdit(link)} title="Edit">&#9998;</button>
                  <button style={{ ...styles.iconBtn, color: '#ef4444' }} onClick={() => deleteLink(link.id)} title="Delete">&#128465;</button>
                </div>
              </div>
            ))}
            {links.length === 0 && (
              <div style={styles.empty}>
                <div style={styles.emptyIcon}>&#128279;</div>
                <p style={styles.emptyTitle}>No links found</p>
                <p style={styles.emptyText}>Add your first link or adjust your filters</p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', background: '#f8fafc', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' },
  topBar: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '16px 32px', background: 'white', borderBottom: '1px solid #e2e8f0', position: 'sticky', top: 0, zIndex: 100 },
  logo: { fontSize: 22, fontWeight: 800, color: '#0f172a', margin: 0 },
  topActions: { display: 'flex', gap: 12 },
  addBtn: { padding: '10px 20px', background: '#0f172a', border: 'none', borderRadius: 10, color: 'white', fontSize: 14, fontWeight: 600, cursor: 'pointer' },
  layout: { display: 'flex', maxWidth: 1200, margin: '0 auto', gap: 32 },
  sidebar: { width: 240, paddingTop: 24 },
  statsCard: { background: 'white', borderRadius: 14, padding: 20, border: '1px solid #e2e8f0', marginBottom: 20 },
  statsTitle: { fontSize: 13, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 16 },
  statRow: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 },
  statNum: { fontSize: 22, fontWeight: 800, color: '#0f172a' },
  statLabel: { fontSize: 13, color: '#64748b' },
  tagsSection: { background: 'white', borderRadius: 14, padding: 20, border: '1px solid #e2e8f0', marginBottom: 16 },
  tagsTitle: { fontSize: 13, fontWeight: 700, color: '#64748b', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 12 },
  tagBtn: { display: 'flex', alignItems: 'center', gap: 8, width: '100%', padding: '7px 10px', background: 'transparent', border: 'none', borderRadius: 8, color: '#475569', cursor: 'pointer', fontSize: 14, marginBottom: 2, textAlign: 'left' },
  tagBtnActive: { background: '#f1f5f9', color: '#0f172a', fontWeight: 600 },
  tagDot: { width: 8, height: 8, borderRadius: '50%', flexShrink: 0 },
  tagCount: { marginLeft: 'auto', fontSize: 12, color: '#94a3b8' },
  favBtn: { width: '100%', padding: '10px 16px', background: 'white', border: '1px solid #e2e8f0', borderRadius: 10, color: '#64748b', cursor: 'pointer', fontSize: 14, fontWeight: 600 },
  favBtnActive: { background: '#fef3c7', border: '1px solid #f59e0b', color: '#b45309' },
  main: { flex: 1, paddingTop: 24, paddingBottom: 40 },
  searchBar: { marginBottom: 20 },
  searchInput: { width: '100%', padding: '12px 18px', background: 'white', border: '1px solid #e2e8f0', borderRadius: 12, fontSize: 15, color: '#0f172a', boxSizing: 'border-box', outline: 'none' },
  addForm: { background: 'white', borderRadius: 14, padding: 24, border: '1px solid #e2e8f0', marginBottom: 20 },
  formTitle: { fontSize: 16, fontWeight: 700, color: '#0f172a', marginBottom: 16 },
  urlInput: { width: '100%', padding: '12px 16px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, fontSize: 15, color: '#0f172a', marginBottom: 10, boxSizing: 'border-box', outline: 'none' },
  input: { width: '100%', padding: '12px 16px', background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 10, fontSize: 15, color: '#0f172a', marginBottom: 10, boxSizing: 'border-box', outline: 'none' },
  formBtns: { display: 'flex', gap: 10, marginTop: 8 },
  cancelBtn: { padding: '10px 20px', background: 'transparent', border: '1px solid #e2e8f0', borderRadius: 10, color: '#64748b', cursor: 'pointer', fontSize: 14 },
  saveBtn: { padding: '10px 24px', background: '#0f172a', border: 'none', borderRadius: 10, color: 'white', cursor: 'pointer', fontSize: 14, fontWeight: 600 },
  linkList: { display: 'flex', flexDirection: 'column', gap: 12 },
  linkCard: { background: 'white', borderRadius: 14, padding: 20, border: '1px solid #e2e8f0', display: 'flex', gap: 16, transition: 'all 0.15s', cursor: 'pointer' },
  linkMain: { flex: 1 },
  linkTitle: { fontSize: 16, fontWeight: 700, color: '#0f172a', marginBottom: 4 },
  linkUrl: { fontSize: 13, color: '#6366f1', marginBottom: 6 },
  linkDesc: { fontSize: 14, color: '#64748b', marginBottom: 8 },
  linkTags: { display: 'flex', flexWrap: 'wrap', gap: 6 },
  tagPill: { fontSize: 11, padding: '2px 8px', borderRadius: 12, fontWeight: 600 },
  linkActions: { display: 'flex', flexDirection: 'column', gap: 8 },
  iconBtn: { width: 32, height: 32, background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: 8, cursor: 'pointer', fontSize: 16, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#64748b' },
  empty: { display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: 80, color: '#94a3b8' },
  emptyIcon: { fontSize: 64, marginBottom: 16 },
  emptyTitle: { fontSize: 18, fontWeight: 700, color: '#64748b', margin: 0 },
  emptyText: { fontSize: 14, color: '#94a3b8' },
};
