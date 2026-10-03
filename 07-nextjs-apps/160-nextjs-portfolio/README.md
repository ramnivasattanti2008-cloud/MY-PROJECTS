# NextJS Portfolio Template

A modern, dark-themed portfolio website built with Next.js 15, TypeScript, Tailwind CSS, and Lucide icons.

## Features

- Hero section with profile and call-to-action
- About section with personal information
- Skills showcase with categories
- Projects grid with hover effects
- Contact form with validation
- Responsive dark theme design
- Smooth scroll navigation

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
nextjs-portfolio/
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── Navbar.tsx
│   ├── Hero.tsx
│   ├── About.tsx
│   ├── Skills.tsx
│   ├── Projects.tsx
│   ├── Contact.tsx
│   └── Footer.tsx
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Components

### Hero
- Profile avatar with gradient background
- Name with animated text
- Tagline and description
- CTA buttons
- Scroll indicator

### About
- Two-column layout
- Profile image placeholder
- Personal information
- Download CV button

### Skills
- Three-column skill categories
- Interactive skill tags
- Statistics section

### Projects
- Grid of project cards
- Gradient backgrounds
- Tags and links
- Hover effects

### Contact
- Contact information cards
- Social media links
- Contact form

## Customization

1. Update personal information in components
2. Replace project data in Projects.tsx
3. Update skills in Skills.tsx
4. Configure social links in Navbar.tsx and Footer.tsx

## License

MIT
