#!/usr/bin/env python3
"""
Video Downloader - Download YouTube videos and audio using yt-dlp

Usage:
    python video-downloader.py <url> [options]

Examples:
    python video-downloader.py "https://www.youtube.com/watch?v=..."
    python video-downloader.py "https://www.youtube.com/watch?v=..." --audio-only
    python video-downloader.py "https://www.youtube.com/watch?v=..." -f "bestvideo[ext=mp4]+bestaudio"
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Run: pip install yt-dlp")
    sys.exit(1)


class VideoDownloader:
    """Handles YouTube video/audio downloading with yt-dlp."""

    def __init__(self, output_dir: str = "downloads"):
        """
        Initialize the downloader.

        Args:
            output_dir: Directory to save downloaded files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_video_info(self, url: str) -> dict:
        """
        Fetch video information without downloading.

        Args:
            url: YouTube video URL

        Returns:
            Dictionary with video metadata
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'description': info.get('description', '')[:500],
                    'thumbnail': info.get('thumbnail', ''),
                    'formats': self._list_formats(info.get('formats', [])),
                }
        except yt_dlp.utils.DownloadError as e:
            raise ValueError(f"Failed to fetch video info: {e}")

    def _list_formats(self, formats: list) -> list:
        """Extract format information from available formats."""
        format_list = []
        for f in formats:
            format_id = f.get('format_id', '')
            ext = f.get('ext', '')
            quality = f.get('format_note', '') or f.get('height', '')
            filesize = f.get('filesize', 0) or 0
            format_list.append({
                'id': format_id,
                'extension': ext,
                'quality': str(quality),
                'size_mb': round(filesize / (1024 * 1024), 2) if filesize else None,
            })
        return format_list[:10]  # Limit to first 10 formats

    def download_video(
        self,
        url: str,
        audio_only: bool = False,
        quality: str = "best",
        format_spec: str = None
    ) -> str:
        """
        Download a video or audio from URL.

        Args:
            url: Video URL
            audio_only: If True, download audio only (mp3)
            quality: Quality preset ('best', '720p', '480p', '360p')
            format_spec: Custom format specification string

        Returns:
            Path to downloaded file
        """
        # Set up output template
        output_template = str(self.output_dir / '%(title)s.%(ext)s')

        # Configure options based on mode
        if audio_only:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_template.replace('.%(ext)s', '.mp3'),
                'nocheckcertificate': True,
            }
        elif format_spec:
            ydl_opts = {
                'format': format_spec,
                'outtmpl': output_template,
                'nocheckcertificate': True,
            }
        else:
            # Quality presets
            quality_formats = {
                'best': 'bestvideo[ext=mp4]+bestaudio/best[ext=mp4]/best',
                '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio/best[height<=720]',
                '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio/best[height<=480]',
                '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio/best[height<=360]',
            }
            ydl_opts = {
                'format': quality_formats.get(quality, quality_formats['best']),
                'outtmpl': output_template,
                'nocheckcertificate': True,
            }

        # Add progress hook
        ydl_opts['progress_hooks'] = [self._progress_hook]

        try:
            print(f"Downloading: {url}")
            print(f"Output directory: {self.output_dir}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

                # Handle post-processed filenames (e.g., .mp3)
                if audio_only:
                    filename = os.path.splitext(filename)[0] + '.mp3'

                return str(filename)

        except yt_dlp.utils.DownloadError as e:
            raise RuntimeError(f"Download failed: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")

    def _progress_hook(self, d: dict):
        """Progress callback for download updates."""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\rProgress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print(f"\nDownload complete! Processing...")

    def download_playlist(
        self,
        playlist_url: str,
        audio_only: bool = False,
        max_videos: int = None
    ) -> list:
        """
        Download an entire playlist.

        Args:
            playlist_url: Playlist URL
            audio_only: If True, download audio only
            max_videos: Maximum number of videos to download

        Returns:
            List of downloaded file paths
        """
        ydl_opts = {
            'quiet': True,
            'nocheckcertificate': True,
        }

        if audio_only:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        if max_videos:
            ydl_opts['playlistend'] = max_videos

        try:
            # First extract playlist info
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                video_count = len(playlist_info.get('entries', []))
                print(f"Playlist contains {video_count} videos")

            # Now download
            ydl_opts['progress_hooks'] = [self._progress_hook]
            ydl_opts['outtmpl'] = str(self.output_dir / '%(playlist_index)s - %(title)s.%(ext)s')

            downloaded = []
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                for entry in ydl.extract_info(playlist_url, download=True)['entries']:
                    if entry:
                        filename = ydl.prepare_filename(entry)
                        downloaded.append(filename)

            print(f"\nDownloaded {len(downloaded)} videos from playlist")
            return downloaded

        except Exception as e:
            raise RuntimeError(f"Playlist download failed: {e}")


def main():
    """Main entry point with CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description='Download YouTube videos and audio',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=..."          Download best quality video
  %(prog)s "https://www.youtube.com/watch?v=..." --audio  Download audio only (mp3)
  %(prog)s "https://www.youtube.com/watch?v=..." -q 720p   Download 720p quality
  %(prog)s "https://www.youtube.com/watch?v=..." --info    Show video info only
        """
    )

    parser.add_argument('url', help='YouTube video or playlist URL')
    parser.add_argument('-o', '--output', default='downloads',
                        help='Output directory (default: downloads)')
    parser.add_argument('-a', '--audio', action='store_true',
                        help='Download audio only (mp3)')
    parser.add_argument('-q', '--quality', default='best',
                        choices=['best', '720p', '480p', '360p'],
                        help='Video quality (default: best)')
    parser.add_argument('-f', '--format', metavar='SPEC',
                        help='Custom format specification (e.g., "bestvideo[ext=mp4]+bestaudio")')
    parser.add_argument('--info', action='store_true',
                        help='Show video info and exit')
    parser.add_argument('-p', '--playlist', action='store_true',
                        help='Download as playlist')
    parser.add_argument('-m', '--max', type=int, metavar='N',
                        help='Maximum videos to download from playlist')

    args = parser.parse_args()

    try:
        downloader = VideoDownloader(args.output)

        if args.info:
            # Show video info only
            print("Fetching video information...\n")
            info = downloader.get_video_info(args.url)
            print(f"Title: {info['title']}")
            print(f"Uploader: {info['uploader']}")
            print(f"Duration: {info['duration']} seconds")
            print(f"Views: {info['view_count']:,}")
            print(f"\nAvailable formats (first 10):")
            for f in info['formats']:
                size = f"{f['size_mb']} MB" if f['size_mb'] else "Unknown"
                print(f"  {f['id']}: {f['quality']} ({f['extension']}) - {size}")
        elif args.playlist:
            # Download playlist
            downloader.download_playlist(
                args.url,
                audio_only=args.audio,
                max_videos=args.max
            )
        else:
            # Download single video
            filepath = downloader.download_video(
                args.url,
                audio_only=args.audio,
                quality=args.quality,
                format_spec=args.format
            )
            print(f"\nSuccess! File saved to: {filepath}")

    except (ValueError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
        sys.exit(130)


if __name__ == '__main__':
    main()
