from spotipy.oauth2 import SpotifyClientCredentials

try:
    from .oauth import client_id, client_secret, ibm_user, ibm_pass
except ImportError:
    client_id = None
    client_secret = None
    ibm_user = None
    ibm_pass = None
credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
ibm = {'u':ibm_user, 'p':ibm_pass}
