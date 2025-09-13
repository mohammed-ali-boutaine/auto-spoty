"""
Spotify module for auto-spoty application.

This module provides functionality to interact with the Spotify API.
"""

from .auth import get_spotify_client
from .manager import SpotifyManager

__all__ = ['SpotifyManager', 'get_spotify_client']