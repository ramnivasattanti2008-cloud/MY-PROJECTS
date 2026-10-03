import React, { useState, useEffect, useCallback } from 'react';

const API_URL = 'http://localhost:5003';

interface User {
  id: number;
  username: string;
  display_name: string;
  bio: string;
  tweet_count?: number;
  followers?: number;
  following?: number;
  tweets?: Tweet[];
}

interface Tweet {
  id: number;
  user_id: number;
  content: string;
  username: string;
  display_name: string;
  likes: number;
  created_at: string;
}

export default function App() {
  const [view, setView] = useState<'feed' | 'profile' | 'users'>('feed');
  const [tweets, setTweets] = useState<Tweet[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [currentUser, setCurrentUser] = useState<string>('alice');
  const [tweetContent, setTweetContent] = useState('');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [newUsername, setNewUsername] = useState('');
  const [newDisplayName, setNewDisplayName] = useState('');
  const [showRegister, setShowRegister] = useState(false);
  const [following, setFollowing] = useState<Set<number>>(new Set());
  const [refreshKey, setRefreshKey] = useState(0);

  const loadFeed = useCallback(() => {
    fetch(`${API_URL}/api/tweets?feed=${currentUser}`)
      .then(r => r.json())
      .then(d => { if (d.success) setTweets(d.data); })
      .catch(() => {});
  }, [currentUser]);

  const loadUsers = useCallback(() => {
    fetch(`${API_URL}/api/users`)
      .then(r => r.json())
      .then(d => { if (d.success) setUsers(d.data); })
      .catch(() => {});
  }, []);

  const loadProfile = useCallback((username: string) => {
    fetch(`${API_URL}/api/users/${username}`)
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setSelectedUser(d.data);
          // Load following state
          const current = users.find(u => u.username === currentUser);
          if (current) {
            setFollowing(prev => {
              const next = new Set(prev);
              d.data.tweets?.forEach(() => next);
              return next;
            });
          }
        }
      })
      .catch(() => {});
  }, [currentUser, users]);

  useEffect(() => { loadFeed(); }, [loadFeed, refreshKey]);
  useEffect(() => { loadUsers(); }, [loadUsers, refreshKey]);
  useEffect(() => {
    if (view === 'profile' && selectedUser) loadProfile(selectedUser.username);
  }, [view, selectedUser, loadProfile, refreshKey]);

  const postTweet = () => {
    if (!tweetContent.trim() || tweetContent.length > 280) return;
    fetch(`${API_URL}/api/tweets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: currentUser, content: tweetContent.trim() }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setTweetContent('');
          loadFeed();
        }
      })
      .catch(() => {});
  };

  const likeTweet = (tweetId: number) => {
    fetch(`${API_URL}/api/tweets/${tweetId}/like`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: currentUser }),
    })
      .then(r => r.json())
      .then(() => loadFeed())
      .catch(() => {});
  };

  const registerUser = () => {
    if (!newUsername.trim() || !newDisplayName.trim()) return;
    fetch(`${API_URL}/api/users`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: newUsername, display_name: newDisplayName }),
    })
      .then(r => r.json())
      .then(d => {
        if (d.success) {
          setNewUsername('');
          setNewDisplayName('');
          setShowRegister(false);
          setCurrentUser(d.data.username);
          loadUsers();
        } else {
          alert(d.error);
        }
      })
      .catch(() => {});
  };

  const followUser = (username: string) => {
    fetch(`${API_URL}/api/follow`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ follower: currentUser, following: username }),
    })
      .then(r => r.json())
      .then(() => {
        setFollowing(prev => { const n = new Set(prev); n.add(selectedUser!.id); return n; });
        loadProfile(selectedUser!.username);
      })
      .catch(() => {});
  };

  const unfollowUser = (username: string) => {
    fetch(`${API_URL}/api/unfollow`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ follower: currentUser, following: username }),
    })
      .then(r => r.json())
      .then(() => {
        setFollowing(prev => { const n = new Set(prev); n.delete(selectedUser!.id); return n; });
        loadProfile(selectedUser!.username);
      })
      .catch(() => {});
  };

  const formatDate = (ts: string) => {
    try {
      const d = new Date(ts);
      const now = new Date();
      const diff = (now.getTime() - d.getTime()) / 1000;
      if (diff < 60) return `${Math.floor(diff)}s`;
      if (diff < 3600) return `${Math.floor(diff / 60)}m`;
      if (diff < 86400) return `${Math.floor(diff / 3600)}h`;
      return d.toLocaleDateString();
    } catch { return ts; }
  };

  return (
    <div style={styles.container}>
      <div style={styles.topBar}>
        <div style={styles.topBarContent}>
          <h1 style={styles.logo}>&#128230; MiniTweet</h1>
          <div style={styles.userSelector}>
            <label style={styles.selectorLabel}>Logged in as:</label>
            <select style={styles.select} value={currentUser} onChange={e => setCurrentUser(e.target.value)}>
              {users.map(u => <option key={u.id} value={u.username}>{u.display_name} (@{u.username})</option>)}
            </select>
            <button style={styles.regBtn} onClick={() => setShowRegister(!showRegister)}>+ Register</button>
          </div>
        </div>
      </div>
      {showRegister && (
        <div style={styles.registerBar}>
          <input style={styles.regInput} type="text" placeholder="username" value={newUsername} onChange={e => setNewUsername(e.target.value.toLowerCase())} />
          <input style={styles.regInput} type="text" placeholder="display name" value={newDisplayName} onChange={e => setNewDisplayName(e.target.value)} />
          <button style={styles.regSubmit} onClick={registerUser}>Join</button>
        </div>
      )}
      <div style={styles.mainLayout}>
        <div style={styles.leftSidebar}>
          <nav style={styles.nav}>
            <button style={{ ...styles.navBtn, ...(view === 'feed' ? styles.navBtnActive : {}) }} onClick={() => setView('feed')}>
              <span style={styles.navIcon}>&#127968;</span> Home
            </button>
            <button style={{ ...styles.navBtn, ...(view === 'users' ? styles.navBtnActive : {}) }} onClick={() => setView('users')}>
              <span style={styles.navIcon}>&#128101;</span> Users
            </button>
          </nav>
        </div>
        <div style={styles.feed}>
          {view === 'feed' && (
            <>
              <div style={styles.composeBox}>
                <textarea
                  style={styles.composeText}
                  placeholder={`What's happening, @${currentUser}?`}
                  value={tweetContent}
                  onChange={e => setTweetContent(e.target.value.slice(0, 280))}
                  rows={3}
                />
                <div style={styles.composeFooter}>
                  <span style={styles.charCount}>{tweetContent.length}/280</span>
                  <button style={{ ...styles.tweetBtn, ...(tweetContent.length > 280 || !tweetContent.trim() ? styles.tweetBtnDisabled : {}) }} onClick={postTweet} disabled={tweetContent.length > 280 || !tweetContent.trim()}>
                    Tweet
                  </button>
                </div>
              </div>
              <div style={styles.tweetList}>
                {tweets.map(tweet => (
                  <div key={tweet.id} style={styles.tweet}>
                    <div style={styles.tweetAvatar}>{tweet.display_name?.charAt(0)?.toUpperCase() || '?'}</div>
                    <div style={styles.tweetBody}>
                      <div style={styles.tweetHeader}>
                        <span style={styles.tweetName}>{tweet.display_name}</span>
                        <span style={styles.tweetHandle}>@{tweet.username}</span>
                        <span style={styles.tweetTime}>{formatDate(tweet.created_at)}</span>
                      </div>
                      <p style={styles.tweetText}>{tweet.content}</p>
                      <div style={styles.tweetActions}>
                        <button style={styles.actionBtn} onClick={() => likeTweet(tweet.id)}>
                          &#10084; {tweet.likes || 0}
                        </button>
                        <button style={styles.actionBtn} onClick={() => { setSelectedUser(users.find(u => u.username === tweet.username) || null); setView('profile'); }}>
                          View Profile
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
                {tweets.length === 0 && <p style={styles.empty}>No tweets yet. Be the first to tweet!</p>}
              </div>
            </>
          )}
          {view === 'users' && (
            <div style={styles.userList}>
              <h2 style={styles.sectionTitle}>All Users</h2>
              {users.map(user => (
                <div key={user.id} style={styles.userCard}>
                  <div style={styles.userAvatar}>{user.display_name?.charAt(0)?.toUpperCase() || '?'}</div>
                  <div style={styles.userInfo}>
                    <div style={styles.userName}>{user.display_name}</div>
                    <div style={styles.userHandle}>@{user.username}</div>
                    {user.bio && <div style={styles.userBio}>{user.bio}</div>}
                  </div>
                  <button style={styles.viewProfileBtn} onClick={() => { setSelectedUser(user); setView('profile'); }}>
                    View
                  </button>
                </div>
              ))}
            </div>
          )}
          {view === 'profile' && selectedUser && (
            <div style={styles.profileView}>
              <button style={styles.backBtn} onClick={() => setView('feed')}>&larr; Back</button>
              <div style={styles.profileHeader}>
                <div style={styles.profileAvatar}>{selectedUser.display_name?.charAt(0)?.toUpperCase() || '?'}</div>
                <div>
                  <h2 style={styles.profileName}>{selectedUser.display_name}</h2>
                  <p style={styles.profileHandle}>@{selectedUser.username}</p>
                  {selectedUser.bio && <p style={styles.profileBio}>{selectedUser.bio}</p>}
                </div>
              </div>
              <div style={styles.profileStats}>
                <span><strong>{selectedUser.tweet_count || 0}</strong> Tweets</span>
                <span><strong>{selectedUser.followers || 0}</strong> Followers</span>
                <span><strong>{selectedUser.following || 0}</strong> Following</span>
              </div>
              {selectedUser.username !== currentUser && (
                following.has(selectedUser.id)
                  ? <button style={styles.unfollowBtn} onClick={() => unfollowUser(selectedUser.username)}>Unfollow</button>
                  : <button style={styles.followBtn} onClick={() => followUser(selectedUser.username)}>Follow</button>
              )}
              <h3 style={styles.tweetsTitle}>Tweets</h3>
              <div>
                {(selectedUser.tweets || []).map(tweet => (
                  <div key={tweet.id} style={styles.tweet}>
                    <div style={styles.tweetAvatar}>{tweet.display_name?.charAt(0)?.toUpperCase() || '?'}</div>
                    <div style={styles.tweetBody}>
                      <div style={styles.tweetHeader}>
                        <span style={styles.tweetName}>{tweet.display_name}</span>
                        <span style={styles.tweetHandle}>@{tweet.username}</span>
                        <span style={styles.tweetTime}>{formatDate(tweet.created_at)}</span>
                      </div>
                      <p style={styles.tweetText}>{tweet.content}</p>
                      <div style={styles.tweetActions}>
                        <span>&#10084; {tweet.likes || 0}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <div style={styles.rightSidebar}>
          <div style={styles.rightCard}>
            <h3 style={styles.rightTitle}>Trending</h3>
            <p style={styles.rightText}>Join the conversation!</p>
            <p style={styles.rightHint}>Demo users: alice, bob, charlie</p>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: { minHeight: '100vh', background: '#f7f9f9', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif' },
  topBar: { background: 'white', borderBottom: '1px solid #eff3f4', position: 'sticky', top: 0, zIndex: 100 },
  topBarContent: { maxWidth: 1200, margin: '0 auto', padding: '12px 24px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' },
  logo: { fontSize: 20, fontWeight: 800, color: '#0f172a', margin: 0 },
  userSelector: { display: 'flex', alignItems: 'center', gap: 10 },
  selectorLabel: { fontSize: 13, color: '#536471' },
  select: { padding: '6px 12px', border: '1px solid #cfd9de', borderRadius: 20, fontSize: 14, color: '#0f172a', background: 'white', cursor: 'pointer' },
  regBtn: { padding: '6px 14px', background: '#0f172a', border: 'none', borderRadius: 20, color: 'white', fontSize: 13, cursor: 'pointer' },
  registerBar: { background: '#f7f9f9', borderBottom: '1px solid #eff3f4', padding: '12px 24px', display: 'flex', gap: 10, justifyContent: 'center' },
  regInput: { padding: '8px 14px', border: '1px solid #cfd9de', borderRadius: 8, fontSize: 14 },
  regSubmit: { padding: '8px 16px', background: '#1d9bf0', border: 'none', borderRadius: 8, color: 'white', fontSize: 14, cursor: 'pointer' },
  mainLayout: { maxWidth: 1200, margin: '0 auto', display: 'flex', gap: 32 },
  leftSidebar: { width: 200, paddingTop: 16 },
  nav: { position: 'sticky', top: 80 },
  navBtn: { display: 'flex', alignItems: 'center', gap: 12, width: '100%', padding: '12px 16px', background: 'transparent', border: 'none', borderRadius: 30, fontSize: 16, fontWeight: 600, color: '#0f172a', cursor: 'pointer', marginBottom: 4 },
  navBtnActive: { background: '#e8f5fe', color: '#1d9bf0' },
  navIcon: { fontSize: 20 },
  feed: { flex: 1, maxWidth: 600, borderLeft: '1px solid #eff3f4', borderRight: '1px solid #eff3f4' },
  composeBox: { background: 'white', borderBottom: '1px solid #eff3f4', padding: 16 },
  composeText: { width: '100%', padding: 12, border: '1px solid #cfd9de', borderRadius: 16, fontSize: 17, resize: 'none', fontFamily: 'inherit', outline: 'none', boxSizing: 'border-box' },
  composeFooter: { display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 12 },
  charCount: { fontSize: 13, color: '#536471' },
  tweetBtn: { padding: '8px 20px', background: '#1d9bf0', border: 'none', borderRadius: 20, color: 'white', fontSize: 14, fontWeight: 700, cursor: 'pointer' },
  tweetBtnDisabled: { background: '#8ecdf8', cursor: 'not-allowed' },
  tweetList: {},
  tweet: { display: 'flex', gap: 12, padding: 16, borderBottom: '1px solid #eff3f4', background: 'white' },
  tweetAvatar: { width: 44, height: 44, borderRadius: '50%', background: '#1d9bf0', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 18, fontWeight: 700, flexShrink: 0 },
  tweetBody: { flex: 1 },
  tweetHeader: { display: 'flex', alignItems: 'center', gap: 4, marginBottom: 4, flexWrap: 'wrap' },
  tweetName: { fontWeight: 700, color: '#0f172a', fontSize: 15 },
  tweetHandle: { color: '#536471', fontSize: 14 },
  tweetTime: { color: '#536471', fontSize: 14 },
  tweetText: { fontSize: 15, color: '#0f172a', margin: '4px 0 8px', lineHeight: 1.5 },
  tweetActions: { display: 'flex', gap: 20 },
  actionBtn: { background: 'transparent', border: 'none', color: '#536471', fontSize: 14, cursor: 'pointer', padding: 0 },
  empty: { textAlign: 'center', padding: 40, color: '#536471' },
  userList: { padding: 16 },
  sectionTitle: { fontSize: 20, fontWeight: 800, color: '#0f172a', marginBottom: 16 },
  userCard: { display: 'flex', alignItems: 'center', gap: 12, padding: 16, background: 'white', borderRadius: 12, marginBottom: 8, border: '1px solid #eff3f4' },
  userAvatar: { width: 48, height: 48, borderRadius: '50%', background: '#6366f1', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 20, fontWeight: 700, flexShrink: 0 },
  userInfo: { flex: 1 },
  userName: { fontWeight: 700, color: '#0f172a' },
  userHandle: { color: '#536471', fontSize: 13 },
  userBio: { fontSize: 13, color: '#536471', marginTop: 4 },
  viewProfileBtn: { padding: '6px 16px', background: '#0f172a', border: 'none', borderRadius: 20, color: 'white', fontSize: 13, cursor: 'pointer' },
  profileView: { padding: 24 },
  backBtn: { padding: '8px 16px', background: 'transparent', border: '1px solid #cfd9de', borderRadius: 20, fontSize: 14, cursor: 'pointer', marginBottom: 20 },
  profileHeader: { display: 'flex', gap: 16, alignItems: 'flex-start', marginBottom: 16 },
  profileAvatar: { width: 80, height: 80, borderRadius: '50%', background: '#6366f1', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32, fontWeight: 700 },
  profileName: { fontSize: 22, fontWeight: 800, color: '#0f172a', margin: 0 },
  profileHandle: { color: '#536471', margin: '4px 0' },
  profileBio: { fontSize: 15, color: '#0f172a', marginTop: 8 },
  profileStats: { display: 'flex', gap: 24, margin: '16px 0', fontSize: 14, color: '#536471' },
  followBtn: { padding: '8px 24px', background: '#0f172a', border: 'none', borderRadius: 20, color: 'white', fontSize: 14, fontWeight: 700, cursor: 'pointer', marginBottom: 20 },
  unfollowBtn: { padding: '8px 24px', background: 'white', border: '1px solid #cfd9de', borderRadius: 20, fontSize: 14, fontWeight: 700, cursor: 'pointer', marginBottom: 20, color: '#0f172a' },
  tweetsTitle: { fontSize: 18, fontWeight: 800, color: '#0f172a', marginBottom: 16 },
  rightSidebar: { width: 300, paddingTop: 16 },
  rightCard: { background: 'white', borderRadius: 16, padding: 20, border: '1px solid #eff3f4', position: 'sticky', top: 80 },
  rightTitle: { fontSize: 18, fontWeight: 800, color: '#0f172a', margin: '0 0 12px' },
  rightText: { fontSize: 14, color: '#536471', margin: '0 0 8px' },
  rightHint: { fontSize: 13, color: '#8ecdf8' },
};
