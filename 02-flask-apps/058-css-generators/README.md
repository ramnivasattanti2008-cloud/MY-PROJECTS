# CSS Generators

A Flask web application with 5 CSS generator tools for developers.

## Features

- **Gradient Generator** - Create linear and radial gradients
- **Box Shadow Generator** - Design depth and shadow effects
- **Button Generator** - Style buttons with custom hover effects
- **Card Generator** - Build modern card components
- **Animation Generator** - Create CSS keyframe animations

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python app.py
```

Then open your browser to `http://127.0.0.1:5000`

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page with all generators |
| `/gradient` | Gradient generator |
| `/box-shadow` | Box shadow generator |
| `/button` | Button style generator |
| `/card` | Card component generator |
| `/animation` | Animation generator |

## Screenshots

Each generator features:
- Live preview panel
- Customizable parameters
- Real-time CSS output
- Copy-to-clipboard functionality
- Preset styles

## Tech Stack

- Python 3.8+
- Flask 3.0+
- Modern CSS3
- Vanilla JavaScript
