# Random User Generator

A React application that fetches and displays random user profiles from the RandomUser.me API.

## Features

- Fetches random user profiles from randomuser.me API
- Displays user avatar, name, and contact information
- Shows location, age, and birthday
- Gender badge with color coding
- Load different numbers of users
- Responsive card-based layout

## Data Displayed

For each user:
- Profile picture (large)
- Full name with title
- Email address (clickable)
- Phone number
- Location (city, state)
- Age
- Date of birth
- Member since date
- Country and nationality

## Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## API

Uses [RandomUser.me](https://randomuser.me/) free API:
- No API key required
- Returns realistic fake user data
- Supports multiple results per request

## Tech Stack

- React 18
- TypeScript
- Vite
- RandomUser.me API
