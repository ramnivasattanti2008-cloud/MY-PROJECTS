import { useState, useEffect, useCallback } from 'react';

interface Quote {
  content: string;
  author: string;
}

const FALLBACK_QUOTES: Quote[] = [
  { content: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
  { content: "Innovation distinguishes between a leader and a follower.", author: "Steve Jobs" },
  { content: "Stay hungry, stay foolish.", author: "Steve Jobs" },
  { content: "The future belongs to those who believe in the beauty of their dreams.", author: "Eleanor Roosevelt" },
  { content: "It is during our darkest moments that we must focus to see the light.", author: "Aristotle" },
  { content: "The only impossible journey is the one you never begin.", author: "Tony Robbins" },
  { content: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" },
  { content: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
  { content: "The best time to plant a tree was 20 years ago. The second best time is now.", author: "Chinese Proverb" },
  { content: "Your time is limited, don't waste it living someone else's life.", author: "Steve Jobs" },
];

export default function App() {
  const [quote, setQuote] = useState<Quote>({ content: '', author: '' });
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const fetchQuote = useCallback(async () => {
    setLoading(true);
    try {
      const response = await fetch('https://api.quotable.io/random');
      if (!response.ok) throw new Error('API unavailable');
      const data = await response.json();
      setQuote({ content: data.content, author: data.author });
    } catch {
      const random = FALLBACK_QUOTES[Math.floor(Math.random() * FALLBACK_QUOTES.length)];
      setQuote(random);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchQuote();
  }, [fetchQuote]);

  const handleShare = async () => {
    const text = `"${quote.content}" - ${quote.author}`;
    if (navigator.share) {
      try {
        await navigator.share({ text });
      } catch {
        await copyToClipboard(text);
      }
    } else {
      await copyToClipboard(text);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      const textarea = document.createElement('textarea');
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.quoteIcon}>&#10077;</div>

        {loading ? (
          <div style={styles.loading}>
            <div style={styles.spinner}></div>
            <p>Loading quote...</p>
          </div>
        ) : (
          <>
            <blockquote style={styles.quote}>
              {quote.content}
            </blockquote>
            <cite style={styles.author}>
              - {quote.author}
            </cite>
          </>
        )}

        <div style={styles.buttons}>
          <button style={styles.newQuoteBtn} onClick={fetchQuote} disabled={loading}>
            New Quote
          </button>
          <button style={styles.shareBtn} onClick={handleShare} disabled={loading}>
            {copied ? 'Copied!' : 'Share'}
          </button>
        </div>
      </div>

      <p style={styles.footer}>
        Powered by Quotable API
      </p>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    backgroundColor: '#0f0f0f',
    display: 'flex',
    flexDirection: 'column',
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
    maxWidth: '600px',
    width: '100%',
    textAlign: 'center',
    position: 'relative',
  },
  quoteIcon: {
    position: 'absolute',
    top: '1.5rem',
    left: '2rem',
    fontSize: '4rem',
    color: '#333',
    lineHeight: 1,
  },
  quote: {
    fontSize: '1.5rem',
    fontWeight: '500',
    color: '#fff',
    lineHeight: 1.6,
    margin: '0 0 1.5rem 0',
    padding: 0,
    fontStyle: 'italic',
  },
  author: {
    display: 'block',
    fontSize: '1rem',
    color: '#888',
    marginBottom: '2rem',
    fontStyle: 'normal',
  },
  buttons: {
    display: 'flex',
    gap: '1rem',
    justifyContent: 'center',
  },
  newQuoteBtn: {
    padding: '0.875rem 2rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: 'none',
    backgroundColor: '#667eea',
    color: '#fff',
    cursor: 'pointer',
    transition: 'transform 0.1s',
  },
  shareBtn: {
    padding: '0.875rem 2rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: '1px solid #333',
    backgroundColor: 'transparent',
    color: '#fff',
    cursor: 'pointer',
    transition: 'transform 0.1s',
  },
  loading: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '1rem',
    color: '#888',
    minHeight: '150px',
    justifyContent: 'center',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '3px solid #333',
    borderTopColor: '#667eea',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
  },
  footer: {
    marginTop: '2rem',
    color: '#555',
    fontSize: '0.875rem',
  },
};
