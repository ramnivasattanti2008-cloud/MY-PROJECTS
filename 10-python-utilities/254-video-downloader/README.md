# Video Downloader

A powerful YouTube video and audio downloader using the yt-dlp library.

## Features

- Download videos in various qualities (best, 720p, 480p, 360p)
- Extract audio as MP3 files
- Custom format specifications
- Playlist downloading
- Video information preview
- Progress tracking with speed and ETA

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install FFmpeg (required for audio extraction):**

   **Windows:**
   ```bash
   winget install ffmpeg
   ```
   Or download from https://ffmpeg.org/download.html

   **macOS:**
   ```bash
   brew install ffmpeg
   ```

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt install ffmpeg
   ```

## Usage

### Download a video (best quality)
```bash
python video-downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Download audio only (MP3)
```bash
python video-downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --audio
```

### Download with specific quality
```bash
python video-downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 720p
```

### Show video info without downloading
```bash
python video-downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" --info
```

### Download a playlist
```bash
python video-downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist
```

### Download playlist with limit
```bash
python video-downloader.py "https://www.youtube.com/playlist?list=PLAYLIST_ID" --playlist --max 5
```

### Custom format specification
```bash
python video-downloader.py "URL" -f "bestvideo[ext=webm]+bestaudio[ext=webm]"
```

### Change output directory
```bash
python video-downloader.py "URL" -o /path/to/folder
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `url` | YouTube video or playlist URL (required) |
| `-o, --output` | Output directory (default: downloads) |
| `-a, --audio` | Download audio only (MP3) |
| `-q, --quality` | Video quality: best, 720p, 480p, 360p |
| `-f, --format` | Custom format specification |
| `--info` | Show video info without downloading |
| `-p, --playlist` | Download as playlist |
| `-m, --max` | Maximum videos from playlist |

## Using as a Python Module

```python
from video-downloader import VideoDownloader

# Initialize downloader
downloader = VideoDownloader("my_downloads")

# Get video info
info = downloader.get_video_info("https://www.youtube.com/watch?v=...")
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']} seconds")

# Download video
filepath = downloader.download_video("https://www.youtube.com/watch?v=...")

# Download audio only
audio_path = downloader.download_video("https://www.youtube.com/watch?v=...", audio_only=True)
```

## Supported Platforms

- YouTube
- YouTube Playlists
- Many other video platforms supported by yt-dlp

## Troubleshooting

**Error: yt-dlp is not installed**
```bash
pip install yt-dlp
```

**Error: FFmpeg not found**
- Make sure FFmpeg is installed and in your system PATH
- Restart your terminal after installing FFmpeg

**Download fails with "Video unavailable"**
- The video might be age-restricted, region-locked, or deleted
- Try with a VPN if the video is region-locked

## License

MIT License - Free to use and modify.
