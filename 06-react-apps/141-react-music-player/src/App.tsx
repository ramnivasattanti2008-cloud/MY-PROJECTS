import { useState, useRef, useEffect } from 'react';

interface Track {
  id: string;
  name: string;
  url: string;
}

export default function App() {
  const [playlist, setPlaylist] = useState<Track[]>([]);
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const audioRef = useRef<HTMLAudioElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handleTimeUpdate = () => setCurrentTime(audio.currentTime);
    const handleLoadedMetadata = () => setDuration(audio.duration);
    const handleEnded = () => {
      if (currentTrack) {
        const currentIndex = playlist.findIndex((t) => t.id === currentTrack.id);
        if (currentIndex < playlist.length - 1) {
          setCurrentTrack(playlist[currentIndex + 1]);
          setIsPlaying(true);
        } else {
          setIsPlaying(false);
        }
      }
    };

    audio.addEventListener('timeupdate', handleTimeUpdate);
    audio.addEventListener('loadedmetadata', handleLoadedMetadata);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate);
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [currentTrack, playlist]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = volume;
    }
  }, [volume]);

  useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play().catch(() => setIsPlaying(false));
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying, currentTrack]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    const newTracks: Track[] = Array.from(files).map((file) => ({
      id: `${Date.now()}-${file.name}`,
      name: file.name.replace(/\.[^/.]+$/, ''),
      url: URL.createObjectURL(file),
    }));

    setPlaylist((prev) => [...prev, ...newTracks]);
    if (!currentTrack && newTracks.length > 0) {
      setCurrentTrack(newTracks[0]);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handlePlayPause = () => {
    if (!currentTrack) return;
    setIsPlaying(!isPlaying);
  };

  const handleTrackSelect = (track: Track) => {
    setCurrentTrack(track);
    setIsPlaying(true);
  };

  const handleRemoveTrack = (trackId: string) => {
    const track = playlist.find((t) => t.id === trackId);
    if (track) {
      URL.revokeObjectURL(track.url);
    }
    setPlaylist((prev) => prev.filter((t) => t.id !== trackId));
    if (currentTrack?.id === trackId) {
      const remaining = playlist.filter((t) => t.id !== trackId);
      setCurrentTrack(remaining[0] || null);
      setIsPlaying(false);
    }
  };

  const handlePrevious = () => {
    if (!currentTrack) return;
    const currentIndex = playlist.findIndex((t) => t.id === currentTrack.id);
    if (currentIndex > 0) {
      setCurrentTrack(playlist[currentIndex - 1]);
      setIsPlaying(true);
    }
  };

  const handleNext = () => {
    if (!currentTrack) return;
    const currentIndex = playlist.findIndex((t) => t.id === currentTrack.id);
    if (currentIndex < playlist.length - 1) {
      setCurrentTrack(playlist[currentIndex + 1]);
      setIsPlaying(true);
    }
  };

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value);
    setCurrentTime(time);
    if (audioRef.current) {
      audioRef.current.currentTime = time;
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div style={styles.container}>
      <audio ref={audioRef} src={currentTrack?.url || ''} />

      <div style={styles.player}>
        <h1 style={styles.title}>Music Player</h1>

        <div style={styles.uploadSection}>
          <input
            ref={fileInputRef}
            type="file"
            accept="audio/*"
            multiple
            onChange={handleFileUpload}
            style={styles.fileInput}
            id="audio-upload"
          />
          <label htmlFor="audio-upload" style={styles.uploadBtn}>
            Upload Audio Files
          </label>
        </div>

        {playlist.length > 0 ? (
          <>
            <div style={styles.nowPlaying}>
              <div style={styles.trackInfo}>
                <div style={styles.musicIcon}>{isPlaying ? '🎵' : '🎶'}</div>
                <div>
                  <p style={styles.trackName}>
                    {currentTrack?.name || 'No track selected'}
                  </p>
                  <p style={styles.trackStatus}>
                    {playlist.length} track{playlist.length !== 1 ? 's' : ''} in playlist
                  </p>
                </div>
              </div>
            </div>

            <div style={styles.progressSection}>
              <span style={styles.time}>{formatTime(currentTime)}</span>
              <input
                type="range"
                min={0}
                max={duration || 0}
                value={currentTime}
                onChange={handleSeek}
                style={styles.progressBar}
              />
              <span style={styles.time}>{formatTime(duration)}</span>
            </div>

            <div style={styles.controls}>
              <button style={styles.controlBtn} onClick={handlePrevious} disabled={!currentTrack}>
                ⏮
              </button>
              <button style={styles.playBtn} onClick={handlePlayPause} disabled={!currentTrack}>
                {isPlaying ? '⏸' : '▶'}
              </button>
              <button style={styles.controlBtn} onClick={handleNext} disabled={!currentTrack}>
                ⏭
              </button>
            </div>

            <div style={styles.volumeSection}>
              <span style={styles.volumeIcon}>🔊</span>
              <input
                type="range"
                min={0}
                max={1}
                step={0.01}
                value={volume}
                onChange={(e) => setVolume(parseFloat(e.target.value))}
                style={styles.volumeSlider}
              />
            </div>

            <div style={styles.playlist}>
              <h3 style={styles.playlistTitle}>Playlist</h3>
              {playlist.map((track, index) => (
                <div
                  key={track.id}
                  style={{
                    ...styles.playlistItem,
                    ...(currentTrack?.id === track.id ? styles.playlistItemActive : {}),
                  }}
                  onClick={() => handleTrackSelect(track)}
                >
                  <span style={styles.playlistNumber}>{index + 1}</span>
                  <span style={styles.playlistName}>{track.name}</span>
                  {currentTrack?.id === track.id && isPlaying && (
                    <span style={styles.playingIndicator}>🎵</span>
                  )}
                  <button
                    style={styles.removeBtn}
                    onClick={(e) => {
                      e.stopPropagation();
                      handleRemoveTrack(track.id);
                    }}
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div style={styles.emptyState}>
            <p style={styles.emptyIcon}>🎵</p>
            <p style={styles.emptyText}>No tracks yet</p>
            <p style={styles.emptySubtext}>Upload audio files to get started</p>
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
  player: {
    backgroundColor: '#1a1a1a',
    borderRadius: '24px',
    padding: '2rem',
    boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
    maxWidth: '450px',
    width: '100%',
  },
  title: {
    color: '#fff',
    fontSize: '1.5rem',
    fontWeight: '600',
    textAlign: 'center',
    marginBottom: '1.5rem',
  },
  uploadSection: {
    marginBottom: '1.5rem',
  },
  fileInput: {
    display: 'none',
  },
  uploadBtn: {
    display: 'block',
    padding: '0.875rem 1.5rem',
    fontSize: '1rem',
    fontWeight: '600',
    borderRadius: '12px',
    border: '2px dashed #333',
    backgroundColor: 'transparent',
    color: '#888',
    cursor: 'pointer',
    textAlign: 'center',
    transition: 'border-color 0.2s',
  },
  nowPlaying: {
    padding: '1rem',
    backgroundColor: '#222',
    borderRadius: '12px',
    marginBottom: '1.5rem',
  },
  trackInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  musicIcon: {
    fontSize: '2rem',
  },
  trackName: {
    color: '#fff',
    fontSize: '1rem',
    fontWeight: '600',
    margin: 0,
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  trackStatus: {
    color: '#888',
    fontSize: '0.75rem',
    margin: '0.25rem 0 0 0',
  },
  progressSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '1.5rem',
  },
  time: {
    color: '#888',
    fontSize: '0.75rem',
    fontVariantNumeric: 'tabular-nums',
    minWidth: '35px',
  },
  progressBar: {
    flex: 1,
    height: '4px',
    WebkitAppearance: 'none',
    background: '#333',
    borderRadius: '2px',
    cursor: 'pointer',
  },
  controls: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1.5rem',
    marginBottom: '1.5rem',
  },
  controlBtn: {
    width: '48px',
    height: '48px',
    fontSize: '1.25rem',
    borderRadius: '50%',
    border: 'none',
    backgroundColor: '#222',
    color: '#fff',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  playBtn: {
    width: '64px',
    height: '64px',
    fontSize: '1.5rem',
    borderRadius: '50%',
    border: 'none',
    backgroundColor: '#667eea',
    color: '#fff',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  volumeSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '1.5rem',
  },
  volumeIcon: {
    fontSize: '1.25rem',
  },
  volumeSlider: {
    flex: 1,
    height: '4px',
    WebkitAppearance: 'none',
    background: '#333',
    borderRadius: '2px',
    cursor: 'pointer',
  },
  playlist: {
    borderTop: '1px solid #333',
    paddingTop: '1.5rem',
  },
  playlistTitle: {
    color: '#fff',
    fontSize: '1rem',
    fontWeight: '600',
    marginBottom: '1rem',
  },
  playlistItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    padding: '0.75rem',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'background-color 0.2s',
  },
  playlistItemActive: {
    backgroundColor: '#222',
  },
  playlistNumber: {
    color: '#666',
    fontSize: '0.875rem',
    width: '20px',
  },
  playlistName: {
    flex: 1,
    color: '#fff',
    fontSize: '0.875rem',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
  },
  playingIndicator: {
    fontSize: '0.875rem',
  },
  removeBtn: {
    padding: '0.25rem 0.5rem',
    fontSize: '0.75rem',
    border: 'none',
    backgroundColor: 'transparent',
    color: '#666',
    cursor: 'pointer',
    borderRadius: '4px',
  },
  emptyState: {
    textAlign: 'center',
    padding: '3rem 1rem',
  },
  emptyIcon: {
    fontSize: '4rem',
    marginBottom: '1rem',
  },
  emptyText: {
    color: '#fff',
    fontSize: '1.25rem',
    fontWeight: '600',
    margin: '0 0 0.5rem 0',
  },
  emptySubtext: {
    color: '#666',
    fontSize: '0.875rem',
    margin: 0,
  },
};
