import typing

import spotipy
from .credentials import credentials

# create a spotipy object
sp = spotipy.Spotify(client_credentials_manager=credentials)

PAGE_SIZE = 50
MAX_PAGE_NUM = 10


def magic_search(q: str, f, limit: int = 50,
                 max_page_num: int = 10):
    """ Searches for a set of tracks given a filter f and a query q. """

    tc = 0
    i = 0

    while tc < limit:

        # find results on the current page
        results = sp.search(q, offset=i * limit, limit=limit)['tracks']['items']

        # yield the ones in the current filter
        for trac in filter(f, results):
            tc += 1
            if tc <= limit:
                yield trac
            else:
                break

        # go to the next page number
        i += 1
        if i >= max_page_num:
            break


def get_songs_with_letter(letter: str, genre: typing.Optional[str] = None):
    """ Gets a spotify song starting with the given letter """

    # build the search string we want to have
    if genre is not None:
        search = "genre:{} AND title:{}*".format(genre, letter[0])
    else:
        search = "title:{}*".format(genre, letter[0])

    # and do a lazy search on all the attributes
    for t in magic_search(search,
                          lambda t: t['name'].lower().startswith(letter[0]), 50,
                          10):
        yield t


ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def get_songs_with_sentence(sentence: str, genre: typing.Optional[str] = None):
    # keep a record of song ids and names we have already picked
    song_ids = []
    song_names = []

    cache = {}

    # iterate over each character in the current sentence
    for s in sentence:
        if s in ALPHABET:

            # if we already requested songs for this letter in the past,
            # we can re-use the existing iterator
            # if not, we need to make a new one here.
            if s not in cache:
                cache[s] = get_songs_with_letter(s, genre=genre)

            while True:
                # take the next element from the given iterator
                # if that fails, we tried all the songs already
                # and have nothing left to try
                try:
                    song = next(cache[s])
                except StopIteration:
                    raise ValueError(
                        'Did not find a song for character {}'.format(s))

                # check if we have the name of id already selected previously
                has_song_id = song['id'] in song_ids
                has_song_name = song['name'] in song_names

                # if we have a new song, we can yield it immediately
                # else, we need to wait for the next iteration
                if not has_song_id and not has_song_name:
                    # store that we have used this song id and name
                    song_ids.append(song['id'])
                    song_names.append(song['name'])

                    # yield the song, and go to the next character
                    yield song
                    break