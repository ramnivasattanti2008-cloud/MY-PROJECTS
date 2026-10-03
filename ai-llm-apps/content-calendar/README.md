# Social Media Content Calendar

Plan, schedule, and track your social media content. Manage posts across platforms and monitor engagement metrics.

## Features

- Add and manage social media posts
- Schedule for multiple platforms (Twitter, Instagram, LinkedIn, Facebook)
- Track post status (Draft, Scheduled, Published)
- Monitor engagement (Likes, Comments)
- Dashboard with metrics overview
- Dark theme with neon accents

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the app:
```bash
streamlit run app.py
```

## Usage

### Adding Posts
1. Click "Add New Post" expander
2. Select platform and date
3. Enter content and hashtags
4. Set status (Draft/Scheduled/Published)
5. Click "Add Post"

### Tracking Engagement
1. Use "Update Engagement" section
2. Select a post
3. Enter likes and comments
4. Click "Update Stats"

### Dashboard Metrics
- Total Posts count
- Scheduled posts
- Published posts
- Draft posts

## Supported Platforms

- Twitter/X
- Instagram
- LinkedIn
- Facebook

## Data Storage

Posts are stored in session state (temporary). For production, integrate with a database.

---

*Built with Streamlit*
