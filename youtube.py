import yt_dlp
import os

def download_from_youtube(query, output_path="downloads/"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path + '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'no_warnings': False,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Search for the song
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            return True, info['title']
        except Exception as e:
            return False, str(e)
        
# download_from_youtube()