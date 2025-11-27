import yt_dlp
import os

# --- Configuration ---
# Create a dedicated directory for your M4A downloads
DOWNLOAD_DIR = str(input("Download directory: "))
# Creates the directory if it doesn't exist (exist_ok=True prevents an error if it already exists)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Prompt the user for the URL(s). Split input by spaces to support multiple links.
URLS = str(input('Input the URL(s) you want to extract (separate multiple URLs with a space): '))

ydl_opts = {
    # 1. JavaScript Runtimes & Challenge Solving
    # The order matters: Deno is tried first, then Node.
    'js_runtimes': {
        'deno': {},  # Deno (recommended) - Add 'path': '/full/path/to/deno' if not in PATH
    },

    # Enables downloading the external solver script (EJS) from GitHub to handle new YouTube challenges
    'remote_components': ['ejs:github'],

    # 2. Format and Output
    'format': 'bestaudio/best',  # Select the best audio-only stream available
    'extract_audio': True,  # Tells yt-dlp to extract the audio stream

    # Define the output path and filename template: ./downloaded_m4a/Video Title.ext
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),

    # 3. Post-processing (Requires FFmpeg)
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',  # Convert the audio to M4A (AAC) format
        'preferredquality': '0',  # Use quality '0' for the highest VBR quality
    },
        {
            'key': 'FFmpegMetadata',
            'add_metadata': True,  # Embeds metadata (title, artist, etc.)
        }],

    # 4. Cleanup and Metadata
    'embedthumbnail': True,  # Embeds the video thumbnail as cover art (Requires FFmpeg)
    # 'addmetadata' is now redundant if FFmpegMetadata is used, but kept for legacy:
    'addmetadata': True,
    'noplaylist': True,  # Ensures only the specified URL(s) are downloaded, not the whole playlist
    'verbose': True  # Set to True for debugging if issues arise
}

# Split the input string into a list of URLs
url_list = URLS.split()

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"\nStarting download of {len(url_list)} URL(s) as high-quality M4A to {DOWNLOAD_DIR}...\n")
        ydl.download(url_list)
        print("\nDownload complete!")
except Exception as e:
    print(f"\nAn error occurred during download: {e}")
