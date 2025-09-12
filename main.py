from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from typing import List, Dict, Any
import webbrowser


# Load environment variables
load_dotenv()

class SpotifyManager:
    def __init__(self):
        
        # access variables
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')
        
        # Check if credentials are loaded
        if not self.client_id or not self.client_secret:
            raise ValueError("Spotify credentials not found in environment variables")
            
        # Check if redirect URI is loaded
        if not self.redirect_uri:
            raise ValueError("Spotify redirect URI not found in environment variables")
        
          
        print(f"using client id : {self.client_id[:10]}....") #show first 10 charact of id
        self.sp = self.authenticate()

        user = self.sp.current_user()
        print(f"Successfully connected as: {user['display_name']}")


        
    
    def authenticate(self) -> spotipy.Spotify:
        """Authenticate with Spotify API"""
        try:
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope="user-library-read playlist-read-private user-read-recently-played",
                cache_path=".spotify_cache",
                show_dialog=True  # Force re-authentication if needed
            )
            
            # Try to get cached token first
            token_info = auth_manager.get_cached_token()
            
            if not token_info:
                # Open browser for authentication
                auth_url = auth_manager.get_authorize_url()
                print(f"Please authenticate here: {auth_url}")
                webbrowser.open(auth_url)
                
                # Wait for user to complete authentication
                input("Press Enter after you've authenticated in the browser...")
                
                # Get the token
                token_info = auth_manager.get_access_token()
            
            return spotipy.Spotify(auth_manager=auth_manager)
            
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise
    
    def get_user_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's playlists with error handling"""
        try:
            playlists = self.sp.current_user_playlists(limit=limit)
            return playlists['items']
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Get tracks from a specific playlist"""
        try:
            results = self.sp.playlist_tracks(playlist_id)
            tracks = []
            
            while results:
                tracks.extend(results['items'])
                # Check if there are more pages
                if results['next']:
                    results = self.sp.next(results)
                else:
                    break
            
            return tracks
        except Exception as e:
            print(f"Error fetching playlist tracks: {e}")
            return []
    
    def get_recently_played(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recently played tracks"""
        try:
            results = self.sp.current_user_recently_played(limit=limit)
            return results['items']
        except Exception as e:
            print(f"Error fetching recently played: {e}")
            return []
    
    def save_playlists_to_file(self, filename: str = "playlists.json"):
        """Save playlists to a JSON file"""
        playlists = self.get_user_playlists()
        
        # Enhance playlist data with track information
        for playlist in playlists:
            playlist['tracks'] = self.get_playlist_tracks(playlist['id'])
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(playlists, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(playlists)} playlists to {filename}")

def main():
    try:
        # Initialize Spotify manager
        spotify_manager = SpotifyManager()
        
        # Get user info
        user = spotify_manager.sp.current_user()
     #    print(f"Connected as: {user['display_name']}")
        print(user)
     #    print(f"Email: {user['email']}")
        print("-" * 50)
        
        # Get and display playlists
        playlists = spotify_manager.get_user_playlists()
        print(f"Found {len(playlists)} playlists:\n")
        
        for i, playlist in enumerate(playlists):
            print(f"{i+1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")
        
        # Save playlists to file
        save_option = input("\nDo you want to save playlists to a file? (y/n): ").lower()
        if save_option == 'y':
            spotify_manager.save_playlists_to_file()
            print("Playlists saved successfully!")
        
        # Show recently played
        recently_played = spotify_manager.get_recently_played()
        if recently_played:
            print(f"\nRecently played tracks:")
            for i, item in enumerate(recently_played[:5]):  # Show first 5
                track = item['track']
                print(f"  {i+1}. {track['name']} by {track['artists'][0]['name']}")
                
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your .env file and Spotify credentials")

if __name__ == "__main__":
    main()