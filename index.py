import re
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://www.beatstars.com/"
}

def get_redirect_url(song_id):
    stream_url = f"https://main.v2.beatstars.com/stream?id={song_id}&return=audio"
    response = requests.get(stream_url, headers=headers, allow_redirects=False)
    
    if 'Location' in response.headers:
        return response.headers['Location']
    
    print("[!] Failed to get redirect URL.")
    quit()

def download_file(url, output_file):
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"File downloaded successfully as {output_file}")
    else:
        print(f"[!] Failed to download file.")

def main():
    beatstars_url = input("Enter the BeatStars link: ")

    found = re.search(r'(\d+)', beatstars_url)
    if not found:
        print("[!] Invalid URL, closing...")
        quit()

    song_id = found.group(1)

    file_url = get_redirect_url(song_id)
    download_file(file_url, f"{song_id}.mp3")

if __name__ == "__main__":
    main()