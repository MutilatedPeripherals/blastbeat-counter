import os
import re
import uuid
from pathlib import Path

from yt_dlp import YoutubeDL


def download_from_youtube_as_mp3(url: str) -> tuple[bool, Path | None]:
    if not re.match(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/', url):
        raise ValueError("The provided URL is not a valid YouTube video URL.")

    output_folder = os.path.join(os.path.dirname(__file__), "tmp")
    os.makedirs(output_folder, exist_ok=True)

    temp_name = str(uuid.uuid4())
    temp_path = os.path.join(output_folder, f"{temp_name}.%(ext)s")

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
            final_path = os.path.join(output_folder, f"{title}.mp3")
            downloaded_path = os.path.join(output_folder, f"{temp_name}.mp3")
            if os.path.exists(downloaded_path):
                os.rename(downloaded_path, final_path)
            return True, Path(final_path)
    except Exception as e:
        print(f"Error: {e}")
        return False, None

if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=K3rDRsEMay0"
    success, path = download_from_youtube_as_mp3(test_url)
    if success:
        print(f"Downloaded file path: {path}")
    else:
        print("Failed to download the video.")
