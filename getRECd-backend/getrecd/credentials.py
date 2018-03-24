from spotipy.oauth2 import SpotifyClientCredentials

try:
    from .oauth import client_id, client_secret, ibm_user, ibm_pass
except ImportError:
    import os
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    ibm_user = os.environ.get('IBM_USER')
    ibm_pass = os.environ.get('IBM_PASS')
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
ibm = {'u':ibm_user, 'p':ibm_pass}
