'use client';

import React, { useState, useEffect, useRef, useCallback } from 'react';

// Styles
const styles = {
  container: {
    display: 'inline-flex',
    alignItems: 'center',
    fontFamily: 'system-ui, -apple-system, sans-serif',
  },
  number: {
    fontVariantNumeric: 'tabular-nums',
    transition: 'color 0.3s ease',
  },
  suffix: {
    marginLeft: '2px',
  },
  prefix: {
    marginRight: '2px',
  },
};

interface AnimatedCounterProps {
  end: number;
  start?: number;
  duration?: number;
  prefix?: string;
  suffix?: string;
  decimals?: number;
  separator?: string;
  prefixColor?: string;
  numberColor?: string;
  suffixColor?: string;
  animateOnView?: boolean;
  triggerOnce?: boolean;
  className?: string;
  onComplete?: () => void;
}

const AnimatedCounter: React.FC<AnimatedCounterProps> = ({
  end,
  start = 0,
  duration = 2000,
  prefix = '',
  suffix = '',
  decimals = 0,
  separator = ',',
  prefixColor,
  numberColor,
  suffixColor,
  animateOnView = true,
  triggerOnce = true,
  className,
  onComplete,
}) => {
  const [count, setCount] = useState(start);
  const [isInView, setIsInView] = useState(!animateOnView);
  const [hasAnimated, setHasAnimated] = useState(false);
  const containerRef = useRef<HTMLSpanElement>(null);
  const rafRef = useRef<number | null>(null);

  const formatNumber = useCallback((num: number): string => {
    const fixed = num.toFixed(decimals);
    const parts = fixed.split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, separator);
    return parts.join('.');
  }, [decimals, separator]);

  const easeOutExpo = (t: number): number => {
    return t === 1 ? 1 : 1 - Math.pow(2, -10 * t);
  };

  useEffect(() => {
    if (!animateOnView) {
      setIsInView(true);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true);
            if (triggerOnce) {
              setHasAnimated(true);
              observer.disconnect();
            }
          } else if (!triggerOnce && !hasAnimated) {
            setIsInView(false);
          }
        });
      },
      { threshold: 0.3 }
    );

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, [animateOnView, triggerOnce, hasAnimated]);

  useEffect(() => {
    if (!isInView || (triggerOnce && hasAnimated && count === end)) {
      return;
    }

    const startTime = performance.now();
    const startValue = count;
    const endValue = end;
    const difference = endValue - startValue;

    const animate = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeOutExpo(progress);
      const currentValue = startValue + difference * easedProgress;

      setCount(currentValue);

      if (progress < 1) {
        rafRef.current = requestAnimationFrame(animate);
      } else {
        setCount(endValue);
        if (onComplete) onComplete();
        if (triggerOnce) setHasAnimated(true);
      }
    };

    rafRef.current = requestAnimationFrame(animate);

    return () => {
      if (rafRef.current) {
        cancelAnimationFrame(rafRef.current);
      }
    };
  }, [isInView, end, duration, triggerOnce, hasAnimated, count, onComplete, start]);

  return (
    <span ref={containerRef} className={className} style={styles.container}>
      {prefix && (
        <span style={{ ...styles.prefix, color: prefixColor }}>{prefix}</span>
      )}
      <span style={{ ...styles.number, color: numberColor }}>
        {formatNumber(count)}
      </span>
      {suffix && (
        <span style={{ ...styles.suffix, color: suffixColor }}>{suffix}</span>
      )}
    </span>
  );
};

// Bonus: AnimatedCounterGroup for multiple counters
interface AnimatedCounterGroupProps {
  items: Array<{
    end: number;
    label: string;
    prefix?: string;
    suffix?: string;
  }>;
  duration?: number;
  animateOnView?: boolean;
  triggerOnce?: boolean;
  containerStyle?: React.CSSProperties;
  itemStyle?: React.CSSProperties;
  labelStyle?: React.CSSProperties;
}

export const AnimatedCounterGroup: React.FC<AnimatedCounterGroupProps> = ({
  items,
  duration = 2000,
  animateOnView = true,
  triggerOnce = true,
  containerStyle,
  itemStyle,
  labelStyle,
}) => {
  return (
    <div
      style={{
        display: 'flex',
        gap: '32px',
        flexWrap: 'wrap',
        justifyContent: 'center',
        ...containerStyle,
      }}
    >
      {items.map((item, index) => (
        <div
          key={index}
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            gap: '8px',
            ...itemStyle,
          }}
        >
          <AnimatedCounter
            end={item.end}
            duration={duration}
            prefix={item.prefix}
            suffix={item.suffix}
            animateOnView={animateOnView}
            triggerOnce={triggerOnce}
          />
          <span style={{ color: '#666', fontSize: '14px', ...labelStyle }}>
            {item.label}
          </span>
        </div>
      ))}
    </div>
  );
};

export default AnimatedCounter;
