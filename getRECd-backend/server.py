from bottle import route, run, static_file
from getrecd import backend
from getrecd.decorators import safe_json
import os
import sys


###
### /api/character/
###


@route('/api/character/<char>/', method='GET')
@safe_json
def character(char):
    return dict(items=list(backend.get_songs_with_letter(char)))


@route('/api/character/<char>/<genre>/', method='GET')
@safe_json
def character_with_genre(char, genre):
    return dict(items=list(backend.get_songs_with_letter(char, genre=genre)))


###
### /api/sentence/
###

@route('/api/sentence/<sentence>/', method='GET')
@safe_json
def sentence(sentence):
    return dict(items=list(backend.get_songs_with_sentence(sentence)))


@route('/api/sentence/<sentence>/<genre>/', method='GET')
@safe_json
def sentence_with_genre(sentence, genre):
    return dict(
        items=list(backend.get_songs_with_sentence(sentence, genre=genre)))


###
### /
###

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')


@route('/public/<path:path>', method='GET')
def static_dir(path):
    return static_file(path, os.path.join(STATIC_PATH, 'public'))


@route('/')
def home_page():
    return static_file('index.html', STATIC_PATH)


###
### MAIN
###

def main(*args):
    host = os.environ['HOST'] if 'HOST' in os.environ else 'localhost'
    port = int(os.environ['PORT']) if 'PORT' in os.environ else 8080
    run(host=host, port=port)


if __name__ == '__main__':
    main(*sys.argv[1:])
