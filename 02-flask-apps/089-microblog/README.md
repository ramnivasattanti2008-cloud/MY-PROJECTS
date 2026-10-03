# Microblog

A Flask-based microblog platform with user authentication, following system, and likes.

## Features

- User registration and login with Flask-Login
- Create short posts (280 characters)
- Follow/unfollow users
- Like posts
- User profiles with stats
- Explore page for all posts
- User settings

## Installation

```bash
cd microblog
pip install -r requirements.txt
python app.py
```

## Demo Accounts

- alice / password123
- bob / password123
- charlie / password123

## Routes

- `/` - Home (redirects to login or timeline)
- `/register` - User registration
- `/login` - User login
- `/logout` - User logout
- `/timeline` - Followed posts feed
- `/explore` - All posts
- `/post` - Create new post (POST)
- `/user/<username>` - User profile
- `/follow/<username>` - Follow/unfollow user (POST)
- `/users` - Discover users
- `/settings` - Account settings
- `/like/<post_id>` - Like/unlike post (POST)
- `/delete_post/<post_id>` - Delete your post (POST)

## Database

Uses SQLite database `microblog.db` with tables:
- `users` - User accounts
- `posts` - Blog posts
- `followers` - Follow relationships
- `likes` - Post likes
