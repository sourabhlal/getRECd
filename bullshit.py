from bottle import route, run, template
from keys import spotify_keys

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


client_credentials_manager = SpotifyClientCredentials(client_id=spotify_keys['client_id'], client_secret=spotify_keys['client_secret'])
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


from bottle import response
from json import dumps
def json(rv):
    response.content_type = 'application/json'
    return dumps(rv)


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)
# 
#
# @route('/recommend/')
# def index(letter):
#     recommendations(seed_artists=None, seed_genres=None, seed_tracks=None, limit=20, country=None, **kwargs)


@route('/things/')
def index():
    results = sp.search(q='weezer', limit=20)
    s = []
    for i, t in enumerate(results['tracks']['items']):
        s.append([i, t])
    return json(s)

run(host='localhost', port=8080)
