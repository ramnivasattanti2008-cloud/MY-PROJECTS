# NextJS Dashboard Template

A modern, dark-themed admin dashboard template built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons.

## Features

- Responsive sidebar navigation
- Dashboard with stats cards
- Data tables with sorting
- Cards for charts and content
- Clean dark theme design
- Modern component architecture

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Theme:** Dark mode

## Getting Started

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Project Structure

```
nextjs-dashboard/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── Sidebar.tsx
│   ├── Header.tsx
│   ├── Card.tsx
│   ├── StatsCard.tsx
│   └── DataTable.tsx
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Components

### Sidebar
Collapsible navigation sidebar with:
- Logo and branding
- Navigation items with icons
- User profile section
- Bottom navigation links

### Header
Top navigation bar with:
- Search functionality
- Notifications with badge
- User avatar

### StatsCard
Display key metrics with:
- Icon
- Value
- Title
- Change percentage with trend indicator

### Card
Generic container for:
- Charts
- Tables
- Content sections

### DataTable
Sortable data table with:
- Column headers
- Status badges
- Hover states

## License

MIT
