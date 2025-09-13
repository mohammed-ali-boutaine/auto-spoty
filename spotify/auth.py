import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()  # load .env once here

def get_spotify_client() -> Spotify:
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
    scope = "user-library-read playlist-read-private user-read-recently-played user-read-playback-state user-modify-playback-state user-read-currently-playing"
    
    # Check if credentials are loaded
    if not client_id or not client_secret:
        raise ValueError("Spotify credentials not found in environment variables")
        
    # Check if redirect URI is loaded
    if not redirect_uri:
        raise ValueError("Spotify redirect URI not found in environment variables")
    
    return Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            cache_path=".spotify_cache",
            show_dialog=True  
        )
    )
