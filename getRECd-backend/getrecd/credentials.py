from spotipy.oauth2 import SpotifyClientCredentials

try:
    from .oauth import client_id, client_secret
except ImportError:
    client_id = None
    client_secret = None

credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
