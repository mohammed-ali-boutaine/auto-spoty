import json
from InquirerPy import inquirer
from spotify import SpotifyManager
from youtube import download_from_youtube
import os


# Menu choices
choices = [
    "Display User Info",
    "Display Playlists",
    "Display Liked Songs",
    "History (Recent Played)",
    "Download Playlist Songs",
    # "Download Song",
    # "Play/Pause Music",
    "Exit"
]


def menu():  # fonctin recursive  with try and except
    while True:
        try:
            print("-"*25, "Menu", "-"*25)
            choice = inquirer.select(
                message="Spotify Menu:",
                choices=choices,
                pointer="👉"
            ).execute()
            return choice
        except Exception as e:
            print(f"Error in menu: {e}, try again...")

def main():
    try:
        # Initialize Spotify manager
        spotify_manager = SpotifyManager()
        
        # Get user info
        user = spotify_manager.get_user_info()
        
        print("User info:")
        print(json.dumps(user, indent=4))
        print("-" * 50)
        while True:
            choice = menu()
            
            # Choice 1 - User Info
            if choice == "Display User Info":
                print("\n" + "=" * 20 + " User Info " + "=" * 20)
                print(f"Display name: {user['display_name']}")
                print(f"Email: {user.get('email', 'Not available')}")
                print(f"Country: {user.get('country', 'Not available')}")
                print(f"Followers: {user['followers']['total']}")
                print(f"Account type: {user['type']}")
                # print(json.dumps(user,indent=4))
                print("=" * 50)
                

            # Choice 2 - Display all playlists
            elif choice == "Display Playlists":
                playlists = spotify_manager.get_user_playlists()
                print(f"\nFound {len(playlists)} playlists:\n")
                
                for i, playlist in enumerate(playlists):
                    print(f"{i+1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")
                
                if playlists:
                    view_playlist = inquirer.confirm(message="View a specific playlist?", default=False).execute()
                    if view_playlist:
                        playlist_index = int(inquirer.number(
                            message="Enter playlist number:",
                            min_allowed=1,
                            max_allowed=len(playlists)
                        ).execute()) - 1
                        
                        selected_playlist = playlists[playlist_index]
                        print(f"\nPlaylist: {selected_playlist['name']}")
                        
                        tracks = spotify_manager.get_playlist_tracks(selected_playlist['id'])
                        print(f"Total tracks: {len(tracks)}")
                        
                        for i, item in enumerate(tracks[:10]):  # Show first 10
                            track = item['track']
                            artists = ", ".join([artist['name'] for artist in track['artists']])
                            print(f"{i+1}. {track['name']} by {artists}")
                        
                        if len(tracks) > 10:
                            print(f"... and {len(tracks) - 10} more tracks")

            # Choice 3 - Liked Songs
            elif choice == "Display Liked Songs":
                print("\nFetching your liked songs...")
                liked_songs = spotify_manager.get_liked_songs()
                
                if not liked_songs:
                    print("No liked songs found or error fetching songs")
                    continue
                
                print(f"\nFound {len(liked_songs)} liked songs:")
                for i, item in enumerate(liked_songs[:15]):  # Show first 15
                    track = item['track']
                    artists = ", ".join([artist['name'] for artist in track['artists']])
                    print(f"{i+1}. {track['name']} by {artists}")
                
                if len(liked_songs) > 15:
                    print(f"... and {len(liked_songs) - 15} more tracks")

            # Choice 4 - History (Recent Played)
            elif choice == "History (Recent Played)":
                recently_played = spotify_manager.get_recently_played(limit=20)
                
                if not recently_played:
                    print("\nNo recently played tracks found")
                    continue
                
                print(f"\nRecently played tracks:")
                for i, item in enumerate(recently_played):
                    track = item['track']
                    artists = ", ".join([artist['name'] for artist in track['artists']])
                    played_at = item['played_at']
                    print(f"{i+1}. {track['name']} by {artists}")
                    print(f"   Played at: {played_at}")
            
            # Choice 5 - Download Playlist Songs
            elif choice == "Download Playlist Songs":
                playlists = spotify_manager.get_user_playlists()
                
                if not playlists:
                    print("\nNo playlists found")
                    continue
                
                print("\nSelect a playlist to download:")
                playlist_choices = [f"{i+1}. {playlist['name']}" for i, playlist in enumerate(playlists)]
                playlist_choice = inquirer.select(
                    message="Select playlist:",
                    choices=playlist_choices,
                ).execute()
                
                playlist_index = int(playlist_choice.split('.')[0]) - 1
                selected_playlist = playlists[playlist_index]
                
                print(f"\nDownloading tracks from '{selected_playlist['name']}'...")
                tracks = spotify_manager.get_playlist_tracks(selected_playlist['id'])
                
                download_path = f"downloads/{selected_playlist['name']}/"
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                
                for i, item in enumerate(tracks):
                    track = item['track']
                    artists = ", ".join([artist['name'] for artist in track['artists']])
                    query = f"{track['name']} {artists}"
                    
                    print(f"Downloading ({i+1}/{len(tracks)}): {query}")
                    success, result = download_from_youtube(query, download_path)
                    
                    if success:
                        print(f"✓ Downloaded: {result}")
                    else:
                        print(f"✗ Failed to download: {result}")
            
            # # Choice 6 - Download Song
            # elif choice == "Download Song":
            #     query = inquirer.text(message="Enter song name to download:").execute()
            #     if query:
            #         print(f"\nSearching and downloading: {query}")
            #         success, result, _ = download_from_youtube(query)
                    
            #         if success:
            #             print(f"✓ Successfully downloaded: {result}")
            #         else:
            #             print(f"✗ Failed to download: {result}")
            
            # # Choice 7 - Play/Pause Music
            # elif choice == "Play/Pause Music":
            #     playback = spotify_manager.get_current_playback()
                
            #     if playback and playback.get('is_playing'):
            #         track = playback['item']
            #         artists = ", ".join([artist['name'] for artist in track['artists']])
            #         print(f"Currently playing: {track['name']} by {artists}")
                    
            #         pause = inquirer.confirm(message="Pause playback?", default=True).execute()
            #         if pause:
            #             spotify_manager.pause_playback()
            #             print("Playback paused")
            #     else:
            #         print("No active playback found")
            #         # Could implement play functionality here if needed
            
            # Choice 8 - Exit
            elif choice == "Exit":
                print("Exiting... 👋")
                break

            elif choice not in choices:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()