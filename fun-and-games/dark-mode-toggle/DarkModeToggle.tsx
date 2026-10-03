'use client';

import React, { useState, useEffect } from 'react';

// Styles
const styles = {
  container: {
    position: 'relative' as const,
    width: '64px',
    height: '32px',
    borderRadius: '16px',
    background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
    cursor: 'pointer',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.3), 0 0 20px rgba(99, 102, 241, 0.3)',
    border: '2px solid rgba(255,255,255,0.1)',
    overflow: 'hidden',
  },
  containerLight: {
    background: 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
    boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1), 0 0 30px rgba(253,160,133,0.5)',
  },
  track: {
    position: 'absolute',
    top: '4px',
    left: '4px',
    right: '4px',
    bottom: '4px',
    borderRadius: '12px',
    background: 'rgba(255,255,255,0.1)',
    overflow: 'hidden',
  },
  stars: {
    position: 'absolute',
    width: '100%',
    height: '100%',
    transition: 'opacity 0.5s ease',
  },
  star: {
    position: 'absolute',
    width: '3px',
    height: '3px',
    borderRadius: '50%',
    background: '#fff',
    animation: 'twinkle 2s ease-in-out infinite',
  },
  cloud: {
    position: 'absolute',
    background: 'rgba(255,255,255,0.9)',
    borderRadius: '50%',
    filter: 'blur(1px)',
    transition: 'opacity 0.5s ease, transform 0.5s ease',
  },
  thumb: {
    position: 'absolute',
    top: '2px',
    width: '26px',
    height: '26px',
    borderRadius: '13px',
    background: 'linear-gradient(135deg, #f6d365 0%, #fda085 50%, #f6d365 100%)',
    boxShadow: '0 2px 8px rgba(0,0,0,0.3), inset 0 -2px 4px rgba(0,0,0,0.1), inset 0 2px 4px rgba(255,255,255,0.5)',
    transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
    zIndex: 2,
  },
  thumbDark: {
    background: 'linear-gradient(135deg, #e2e2e2 0%, #c9c9c9 50%, #e2e2e2 100%)',
    boxShadow: '0 2px 8px rgba(0,0,0,0.4), inset 0 -2px 4px rgba(0,0,0,0.1), inset 0 2px 4px rgba(255,255,255,0.3)',
  },
  sunRays: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    width: '100%',
    height: '100%',
    transform: 'translate(-50%, -50%)',
    transition: 'opacity 0.4s ease',
  },
  ray: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    width: '2px',
    height: '8px',
    background: 'rgba(255,255,255,0.8)',
    borderRadius: '1px',
    transformOrigin: 'center 12px',
  },
  label: {
    position: 'absolute',
    width: '1px',
    height: '1px',
    padding: 0,
    margin: '-1px',
    overflow: 'hidden',
    clip: 'rect(0,0,0,0)',
    whiteSpace: 'nowrap',
    border: 0,
  },
};

interface DarkModeToggleProps {
  onToggle?: (isDark: boolean) => void;
  defaultDark?: boolean;
  size?: 'small' | 'medium' | 'large';
}

const DarkModeToggle: React.FC<DarkModeToggleProps> = ({
  onToggle,
  defaultDark = false,
  size = 'medium',
}) => {
  const [isDark, setIsDark] = useState(defaultDark);

  useEffect(() => {
    const saved = localStorage.getItem('theme');
    if (saved) {
      setIsDark(saved === 'dark');
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setIsDark(prefersDark);
    }
  }, []);

  useEffect(() => {
    const theme = isDark ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
    document.body.classList.toggle('dark-mode', isDark);
    onToggle?.(isDark);
  }, [isDark, onToggle]);

  const sizeConfig = {
    small: { width: 48, height: 24, thumbSize: 20 },
    medium: { width: 64, height: 32, thumbSize: 26 },
    large: { width: 80, height: 40, thumbSize: 34 },
  };

  const config = sizeConfig[size];

  const handleClick = () => {
    setIsDark(!isDark);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  const stars = [
    { top: '15%', left: '20%', delay: '0s', size: '2px' },
    { top: '25%', left: '70%', delay: '0.3s', size: '2.5px' },
    { top: '60%', left: '30%', delay: '0.6s', size: '2px' },
    { top: '70%', left: '80%', delay: '0.9s', size: '1.5px' },
    { top: '40%', left: '50%', delay: '1.2s', size: '2px' },
  ];

  const rays = Array.from({ length: 8 }, (_, i) => ({
    transform: `translate(-50%, -50%) rotate(${i * 45}deg) translateY(-12px)`,
  }));

  const sunSize = size === 'small' ? 10 : size === 'large' ? 16 : 12;

  return (
    <>
      <style>
        {`
          @keyframes twinkle {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.3; transform: scale(0.8); }
          }
          @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
          }
        `}
      </style>
      <div
        role="switch"
        aria-checked={isDark}
        aria-label="Toggle dark mode"
        tabIndex={0}
        onClick={handleClick}
        onKeyDown={handleKeyDown}
        style={{
          ...styles.container,
          width: `${config.width}px`,
          height: `${config.height}px`,
          borderRadius: `${config.height / 2}px`,
          ...(isDark ? {} : styles.containerLight),
        }}
      >
        {/* Stars (visible in dark mode) */}
        <div style={{
          ...styles.stars,
          opacity: isDark ? 1 : 0,
        }}>
          {stars.map((star, i) => (
            <div
              key={i}
              style={{
                ...styles.star,
                top: star.top,
                left: star.left,
                width: star.size,
                height: star.size,
                animationDelay: star.delay,
              }}
            />
          ))}
        </div>

        {/* Sun rays (visible in light mode) */}
        <div style={{
          ...styles.sunRays,
          opacity: isDark ? 0 : 1,
        }}>
          {rays.map((ray, i) => (
            <div
              key={i}
              style={{
                ...styles.ray,
                transform: ray.transform,
              }}
            />
          ))}
        </div>

        {/* Thumb */}
        <div
          style={{
            ...styles.thumb,
            ...(isDark ? styles.thumbDark : {}),
            width: `${config.thumbSize}px`,
            height: `${config.thumbSize}px`,
            borderRadius: `${config.thumbSize / 2}px`,
            left: isDark ? `${config.width - config.thumbSize - 4}px` : '3px',
            transform: isDark ? 'rotate(360deg)' : 'rotate(0deg)',
          }}
        >
          {/* Sun/Moon icon inside thumb */}
          {isDark ? (
            <svg
              viewBox="0 0 24 24"
              style={{
                width: '60%',
                height: '60%',
                position: 'absolute',
                top: '20%',
                left: '20%',
                fill: '#f6d365',
              }}
            >
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
          ) : (
            <svg
              viewBox="0 0 24 24"
              style={{
                width: '60%',
                height: '60%',
                position: 'absolute',
                top: '20%',
                left: '20%',
                fill: '#fff',
              }}
            >
              <circle cx="12" cy="12" r="5" />
              <line x1="12" y1="1" x2="12" y2="3" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="12" y1="21" x2="12" y2="23" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="1" y1="12" x2="3" y2="12" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="21" y1="12" x2="23" y2="12" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
            </svg>
          )}
        </div>

        <span style={styles.label as React.CSSProperties}>
          {isDark ? 'Dark mode enabled' : 'Light mode enabled'}
        </span>
      </div>
    </>
  );
};

export default DarkModeToggle;
