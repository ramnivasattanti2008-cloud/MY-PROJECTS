import { useState, useEffect } from 'react'

interface User {
  login: {
    uuid: string
  }
  name: {
    title: string
    first: string
    last: string
  }
  picture: {
    large: string
    medium: string
    thumbnail: string
  }
  email: string
  phone: string
  location: {
    city: string
    state: string
    country: string
  }
  dob: {
    date: string
    age: number
  }
  registered: {
    date: string
  }
  gender: string
  nat: string
}

function App() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchUsers = async (count: number = 6) => {
    setLoading(true)
    setError('')

    try {
      const response = await fetch(`https://randomuser.me/api/?results=${count}`)
      const data = await response.json()

      if (data.results) {
        setUsers(data.results)
      } else {
        setError('Failed to fetch users')
      }
    } catch {
      setError('Network error. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchUsers()
  }, [])

  const getAge = (dateString: string) => {
    const date = new Date(dateString)
    const ageDifMs = Date.now() - date.getTime()
    const ageDate = new Date(ageDifMs)
    return Math.abs(ageDate.getUTCFullYear() - 1970)
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  }

  const getGenderIcon = (gender: string) => {
    return gender === 'male' ? 'Male' : 'Female'
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1 style={styles.title}>Random User Generator</h1>
        <p style={styles.subtitle}>Discover people from around the world</p>
      </div>

      <div style={styles.controls}>
        <button
          onClick={() => fetchUsers()}
          disabled={loading}
          style={styles.refreshButton}
        >
          {loading ? 'Loading...' : 'Refresh Users'}
        </button>
        <button
          onClick={() => fetchUsers(12)}
          disabled={loading}
          style={styles.moreButton}
        >
          Load 12 Users
        </button>
      </div>

      {error && <div style={styles.error}>{error}</div>}

      <div style={styles.grid}>
        {users.map((user) => (
          <div key={user.login.uuid} style={styles.card}>
            <div style={styles.avatarContainer}>
              <img
                src={user.picture.large}
                alt={`${user.name.first} ${user.name.last}`}
                style={styles.avatar}
              />
              <span
                style={{
                  ...styles.genderBadge,
                  backgroundColor: user.gender === 'male' ? '#3b82f6' : '#ec4899',
                }}
              >
                {getGenderIcon(user.gender)}
              </span>
            </div>

            <div style={styles.cardContent}>
              <h3 style={styles.name}>
                {user.name.title} {user.name.first} {user.name.last}
              </h3>

              <div style={styles.infoGrid}>
                <div style={styles.infoItem}>
                  <span style={styles.infoIcon}>Email</span>
                  <a href={`mailto:${user.email}`} style={styles.infoValue}>
                    {user.email}
                  </a>
                </div>

                <div style={styles.infoItem}>
                  <span style={styles.infoIcon}>Phone</span>
                  <span style={styles.infoValue}>{user.phone}</span>
                </div>

                <div style={styles.infoItem}>
                  <span style={styles.infoIcon}>Location</span>
                  <span style={styles.infoValue}>
                    {user.location.city}, {user.location.state}
                  </span>
                </div>

                <div style={styles.infoItem}>
                  <span style={styles.infoIcon}>Age</span>
                  <span style={styles.infoValue}>{user.dob.age} years old</span>
                </div>

                <div style={styles.infoItem}>
                  <span style={styles.infoIcon}>Birthday</span>
                  <span style={styles.infoValue}>
                    {formatDate(user.dob.date)}
                  </span>
                </div>

                <div style={styles.infoItem}>
                  <span style={styles.infoIcon}>Member Since</span>
                  <span style={styles.infoValue}>
                    {formatDate(user.registered.date)}
                  </span>
                </div>
              </div>

              <div style={styles.footer}>
                <span style={styles.country}>Country: {user.location.country}</span>
                <span style={styles.nat}>Nationality: {user.nat}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {users.length > 0 && (
        <div style={styles.footer}>
          <button
            onClick={() => fetchUsers()}
            disabled={loading}
            style={styles.refreshButtonBottom}
          >
            Generate More Users
          </button>
        </div>
      )}
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#f8fafc',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    padding: '40px 20px',
  },
  header: {
    textAlign: 'center' as const,
    marginBottom: '32px',
  },
  title: {
    color: '#1e293b',
    fontSize: '36px',
    fontWeight: 700,
    marginBottom: '8px',
  },
  subtitle: {
    color: '#64748b',
    fontSize: '18px',
  },
  controls: {
    display: 'flex',
    justifyContent: 'center',
    gap: '16px',
    marginBottom: '32px',
    flexWrap: 'wrap' as const,
  },
  refreshButton: {
    padding: '14px 28px',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  moreButton: {
    padding: '14px 28px',
    backgroundColor: '#10b981',
    color: '#ffffff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  error: {
    backgroundColor: '#fef2f2',
    color: '#dc2626',
    padding: '12px 20px',
    borderRadius: '10px',
    textAlign: 'center' as const,
    marginBottom: '24px',
    maxWidth: '600px',
    margin: '0 auto 24px',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))',
    gap: '24px',
    maxWidth: '1400px',
    margin: '0 auto',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '20px',
    overflow: 'hidden',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
    transition: 'transform 0.2s, box-shadow 0.2s',
  },
  avatarContainer: {
    position: 'relative',
    display: 'flex',
    justifyContent: 'center',
    paddingTop: '24px',
    backgroundColor: '#f1f5f9',
  },
  avatar: {
    width: '120px',
    height: '120px',
    borderRadius: '50%',
    border: '4px solid #ffffff',
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
  },
  genderBadge: {
    position: 'absolute',
    bottom: '12px',
    padding: '4px 12px',
    borderRadius: '12px',
    color: '#ffffff',
    fontSize: '12px',
    fontWeight: 600,
  },
  cardContent: {
    padding: '20px',
  },
  name: {
    color: '#1e293b',
    fontSize: '20px',
    fontWeight: 700,
    textAlign: 'center' as const,
    marginBottom: '16px',
  },
  infoGrid: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
  },
  infoItem: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '2px',
  },
  infoIcon: {
    color: '#94a3b8',
    fontSize: '11px',
    fontWeight: 600,
    textTransform: 'uppercase' as const,
    letterSpacing: '0.5px',
  },
  infoValue: {
    color: '#475569',
    fontSize: '14px',
    wordBreak: 'break-word' as const,
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: '12px',
    paddingTop: '12px',
    borderTop: '1px solid #e2e8f0',
  },
  country: {
    color: '#64748b',
    fontSize: '12px',
  },
  nat: {
    color: '#64748b',
    fontSize: '12px',
  },
  refreshButtonBottom: {
    padding: '14px 28px',
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
    borderRadius: '10px',
    fontSize: '16px',
    fontWeight: 600,
    cursor: 'pointer',
    margin: '32px auto 0',
    display: 'block',
  },
}

export default App
