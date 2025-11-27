import yt_dlp
import os

# --- Configuration ---
DOWNLOAD_DIR = str(input("Download directory: "))
ARCHIVE_FILE = 'download_history.txt'  # File to track downloaded videos
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

URLS = str(input('Input the YouTube Playlist URL or Video URL(s): '))

ydl_opts = {
    # 1. JavaScript Runtimes & Challenge Solving
    'js_runtimes': {
        'deno': {},
    },
    'remote_components': ['ejs:github'],

    # 2. Format and Output
    'format': 'bestaudio/best',
    'extract_audio': True,

    # Organizes files by playlist title, saving them under the main folder
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(playlist_title)s', '%(title)s.%(ext)s'),

    # NEW FEATURE 1: Skips videos & audios already listed in the archive file
    'download_archive': ARCHIVE_FILE,

    # 3. Post-processing (Requires FFmpeg)
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '0',
    },
        {
            'key': 'FFmpegMetadata',
            'add_metadata': True,
        }],

    # 4. Playlist Handling
    'embedthumbnail': True,
    'addmetadata': True,
    # REMOVED: 'noplaylist': True  <-- We need to remove this to allow playlist downloads
    # NEW FEATURE 2: Control which parts of the playlist to download
    'playlist_items': '1-',  # Example: Download items from index 10 through 20
    'ignoreerrors': True,  # Good practice for playlists: skip failed videos and continue
}

# Split the input string into a list of URLs
url_list = URLS.split()

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\nStarting download of {len(url_list)} URL(s) / Playlists to {DOWNLOAD_DIR}...\n")
        ydl.download(url_list)
        print("\nDownload complete!")
except Exception as e:
    print(f"\nAn error occurred during download: {e}")