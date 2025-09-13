from typing import List, Dict, Any, Optional
from .auth import get_spotify_client

class SpotifyManager:
    def __init__(self):
        """Initialize the SpotifyManager and authenticate"""
        try:
            self.sp = get_spotify_client()
            user = self.sp.current_user()
            print(f"Successfully connected as: {user['display_name']}")
        except Exception as e:
            print(f"Authentication failed: {e}")
            raise
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user profile information"""
        try:
            return self.sp.current_user()
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return {}
    
    def get_user_playlists(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's playlists with pagination support"""
        try:
            playlists = []
            offset = 0

            while True:
                response = self.sp.current_user_playlists(limit=limit, offset=offset)
                items = response.get("items", [])
                if not items:
                    break  # no more playlists
                playlists.extend(items)
                offset += limit  # move to next batch
                
                # Break if we've reached the end
                if len(items) < limit:
                    break
            
            return playlists
        except Exception as e:
            print(f"Error fetching playlists: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict[str, Any]]:
        """Get tracks from a specific playlist with pagination support"""
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
    
    def get_liked_songs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's liked/saved tracks"""
        try:
            tracks = []
            offset = 0
            
            while True:
                results = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
                items = results.get('items', [])
                if not items:
                    break
                
                tracks.extend(items)
                offset += limit
                
                # Break if we've reached the end
                if len(items) < limit:
                    break
                    
            return tracks
        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            return []
            

            

            

    