# Mini Twitter

A lightweight Twitter clone with tweets, follows, likes, and a social feed.

## Features

- Post tweets (280 character limit)
- Follow/unfollow users
- Like tweets
- Social feed showing followed users' tweets
- User profiles with stats
- Register new users
- Pre-seeded demo users (alice, bob, charlie)

## Tech Stack

- **Backend**: Flask, Flask-CORS, SQLite
- **Frontend**: React, TypeScript
- **Database**: SQLite (auto-created with demo data)

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API runs on `http://localhost:5003`

### Frontend

```bash
cd frontend
npm install
npm start
```

The app runs on `http://localhost:3002`

## Demo Users

The app comes pre-seeded with three demo users:

- **Alice Johnson** (@alice)
- **Bob Smith** (@bob)
- **Charlie Brown** (@charlie)

Switch between users using the dropdown in the top bar.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | List all users |
| POST | `/api/users` | Register new user |
| GET | `/api/users/<username>` | Get user profile |
| GET | `/api/tweets` | Get all tweets |
| GET | `/api/tweets?feed=<username>` | Get feed for user |
| POST | `/api/tweets` | Post a tweet |
| POST | `/api/tweets/<id>/like` | Like a tweet |
| POST | `/api/follow` | Follow a user |
| POST | `/api/unfollow` | Unfollow a user |
