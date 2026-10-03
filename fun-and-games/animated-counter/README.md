# Animated Counter Component

A React component that animates numbers when scrolled into view, with smooth easing and various customization options.

## Features

- Smooth counting animation with easeOutExpo easing
- Scroll-triggered animation (Intersection Observer)
- Number formatting with separators and decimals
- Prefix/suffix support (e.g., "$", "%", "+")
- Customizable colors
- Group multiple counters together
- Completion callback
- Trigger once or repeat on scroll

## Installation

Copy `AnimatedCounter.tsx` into your React/Next.js project.

## Usage

### Basic Usage

```tsx
import AnimatedCounter from '@/components/AnimatedCounter';

function Stats() {
  return (
    <div>
      <AnimatedCounter end={1000} />
    </div>
  );
}
```

### With Prefix and Suffix

```tsx
<AnimatedCounter 
  end={99.9} 
  decimals={1}
  suffix="%" 
/>
// Output: 99.9%

<AnimatedCounter 
  end={1500} 
  prefix="$" 
  suffix="+"
/>
// Output: $1,500+
```

### Currency Formatting

```tsx
<AnimatedCounter 
  end={1000000} 
  prefix="$" 
  separator=","
/>
// Output: $1,000,000
```

### Disable Scroll Animation

```tsx
<AnimatedCounter 
  end={500} 
  animateOnView={false}
  start={0}
  duration={3000}
/>
```

### With Completion Callback

```tsx
<AnimatedCounter 
  end={100} 
  onComplete={() => console.log('Animation complete!')}
/>
```

### Multiple Counters (CounterGroup)

```tsx
import { AnimatedCounterGroup } from '@/components/AnimatedCounter';

const stats = [
  { end: 10000, label: 'Users', suffix: '+' },
  { end: 500, label: 'Projects', suffix: '+' },
  { end: 99, label: 'Satisfaction', suffix: '%', decimals: 1 },
];

<AnimatedCounterGroup items={stats} duration={2000} />
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `end` | `number` | **required** | Target number to count to |
| `start` | `number` | `0` | Starting number |
| `duration` | `number` | `2000` | Animation duration in ms |
| `prefix` | `string` | - | Text before the number |
| `suffix` | `string` | - | Text after the number |
| `decimals` | `number` | `0` | Decimal places |
| `separator` | `string` | `,` | Thousands separator |
| `prefixColor` | `string` | - | CSS color for prefix |
| `numberColor` | `string` | - | CSS color for number |
| `suffixColor` | `string` | - | CSS color for suffix |
| `animateOnView` | `boolean` | `true` | Trigger on scroll into view |
| `triggerOnce` | `boolean` | `true` | Only trigger animation once |
| `className` | `string` | - | CSS class for container |
| `onComplete` | `() => void` | - | Callback when animation ends |

## AnimatedCounterGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `items` | `Array` | **required** | Array of counter configs |
| `duration` | `number` | `2000` | Animation duration in ms |
| `animateOnView` | `boolean` | `true` | Trigger on scroll |
| `triggerOnce` | `boolean` | `true` | Only trigger once |
| `containerStyle` | `CSSProperties` | - | Container styles |
| `itemStyle` | `CSSProperties` | - | Individual item styles |
| `labelStyle` | `CSSProperties` | - | Label text styles |

## Example: Stats Section

```tsx
function StatsSection() {
  return (
    <section style={{ padding: '60px 20px', textAlign: 'center' }}>
      <h2 style={{ marginBottom: '40px', fontSize: '32px' }}>
        Our Impact
      </h2>
      <AnimatedCounterGroup
        items={[
          { end: 50000, label: 'Downloads', suffix: '+' },
          { end: 1200, label: 'Happy Clients' },
          { end: 98, label: 'Satisfaction Rate', suffix: '%', decimals: 1 },
          { end: 15, label: 'Years Experience', suffix: '+' },
        ]}
        containerStyle={{ maxWidth: '800px', margin: '0 auto' }}
        itemStyle={{ 
          padding: '20px',
          background: '#f5f5f5',
          borderRadius: '12px',
        }}
        labelStyle={{ fontWeight: 500 }}
      />
    </section>
  );
}
```

## How It Works

1. Uses `IntersectionObserver` to detect when component enters viewport
2. Uses `requestAnimationFrame` for smooth 60fps animation
3. Applies `easeOutExpo` easing for natural deceleration
4. Supports number formatting with locale-aware separators
