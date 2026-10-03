# NextJS Blog Template

A modern, dark-themed blog template built with Next.js 15, TypeScript, MDX, and Tailwind CSS.

## Features

- MDX support for writing blog posts
- Category filtering
- Responsive dark theme design
- Reading time estimates
- Modern component architecture
- Easy-to-customize styling

## Tech Stack

- **Framework:** Next.js 15 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Content:** MDX
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

## Writing Posts

Create new blog posts in the `content/posts/` directory with `.mdx` extension:

```mdx
---
title: "Your Post Title"
date: "2024-01-15"
excerpt: "A brief description of your post."
category: "Tutorial"
readingTime: "5 min read"
---

Your content here...
```

## Project Structure

```
nextjs-blog/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── BlogList.tsx
│   ├── BlogCard.tsx
│   └── CategoryFilter.tsx
├── content/
│   └── posts/
│       └── *.mdx
├── lib/
│   └── posts.ts
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## License

MIT
