# Flask Event Manager

An event management application with RSVP functionality and calendar view.

## Features

- Create events with date, time, and location
- View events in list or calendar format
- RSVP functionality (attending, maybe, not attending)
- Track guest counts
- Clean, modern interface

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Open http://localhost:5000 in your browser.

## Routes

- `/` - View events (list or calendar view)
- `/event/<id>` - View event details and RSVPs
- `/create` - Create a new event
- `/rsvp/<id>` - RSVP to an event
- `/delete/<id>` - Delete an event

## Views

Toggle between list view and calendar view using the URL parameter:
- `/?view=list` - List view (default)
- `/?view=calendar` - Calendar view

Navigate calendar months using prev/next links.
