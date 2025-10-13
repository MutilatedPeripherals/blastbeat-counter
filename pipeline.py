import argparse
from pathlib import Path

from downloading import download_from_youtube_as_mp3
from processing import process_song

parser = argparse.ArgumentParser()
parser.add_argument("--urls", action="store_true")
args = parser.parse_args()

paths = []
if args.urls:
    with open("urls.txt", "r") as f:
        urls = [line.strip() for line in f if line.strip()]
    for url in urls:
        print(f"Processing URL: {url}")
        success, file_path = download_from_youtube_as_mp3(url)
        if not success or file_path is None:
            print(f"Failed to download: {url}")
            continue
        print(f"Downloaded file to: {file_path}")
        paths.append(file_path)
else:
    with open("localfiles.txt", "r") as f:
        files = [line.strip() for line in f if line.strip()]
    for path_str in files:
        file_path = Path(path_str)
        if not file_path.exists():
            print(f"File does not exist: {file_path}")
            continue
        paths.append(file_path)

print(f"Processing {len(paths)} files...")
for path in paths:
    process_song(path, EXPERIMENTAL_BOOST_DRUM_FREQUENCIES=False)
    print("-----")
