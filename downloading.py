import json
import re
import uuid
from pathlib import Path

from yt_dlp import YoutubeDL

CACHE_FILE = Path(__file__).parent / "cache.json"

def download_from_youtube_as_mp3(url: str) -> tuple[bool, Path | None]:
    if not re.match(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/', url):
        raise ValueError("The provided URL is not a valid YouTube video URL.")

    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    else:
        cache = {}

    if url in cache:
        print("Using cached download.")
        cached_path = Path(cache[url])
        if cached_path.exists():
            return True, cached_path

    output_folder = Path(__file__).parent / "tmp"
    output_folder.mkdir(exist_ok=True)

    temp_name = str(uuid.uuid4())
    temp_path = str(output_folder / f"{temp_name}.%(ext)s")

    opts = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "outtmpl": temp_path,
        "quiet": False,
    }

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = re.sub(r'[<>:"/\\|?*]', ' ', info['title'])
            final_path = output_folder / f"{title}.mp3"
            downloaded_path = output_folder / f"{temp_name}.mp3"
            if downloaded_path.exists():
                downloaded_path.rename(final_path)
            cache[url] = str(final_path)
            with open(CACHE_FILE, "w") as f:
                json.dump(cache, f, indent=2)
            return True, final_path
    except Exception as e:
        print(f"Error: {e}")
        return False, None
