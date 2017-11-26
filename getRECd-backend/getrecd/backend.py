
import spotipy
from .credentials import credentials, ibm

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, \
    EmotionOptions, SentimentOptions

# create a spotipy object
sp = spotipy.Spotify(client_credentials_manager=credentials)

PAGE_SIZE = 50
MAX_PAGE_NUM = 100


def magic_search(q, f, limit=50, max_page_num=10):
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


def sort_iterable_chunks(iterable, sort, chunk_size=10):
    """ Sorts each chunk of a the iterable of a certain size. """
    exit = False

    while not exit:
        chunks = []

        for i in range(chunk_size):
            try:
                chunks.append(next(iterable))
            except StopIteration:
                exit = True
                break

        for item in sort(chunks):
            yield item


def get_songs_with_letter(letter, genre=None):
    """ Gets a spotify song starting with the given letter """

    letter = letter[0].lower()

    # build the search string we want to have
    if genre is not None:
        search = "genre:{} AND name:{}*".format(genre, letter)
    else:
        search = "name:{}*".format(letter)

    # and do a lazy search on all the attributes
    for t in magic_search(search,
                          lambda t: t['name'].lower().startswith(letter),
                          PAGE_SIZE, MAX_PAGE_NUM):
        yield t


ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def get_songs_with_sentence(sentence, genre=None):
    # keep a record of song ids and names we have already picked
    song_ids = []
    song_names = []

    cache = {}
    try:
        sentiment = get_sentiment(sentence)
    except:
        sentiment = None

    # iterate over each character in the current sentence
    for s in sentence:
        s = s.lower()
        if s in ALPHABET:

            # if we already requested songs for this letter in the past,
            # we can re-use the existing iterator
            # if not, we need to make a new one here.
            if s not in cache:
                if sentiment is not None:
                    cache[s] = sort_iterable_chunks(
                        get_songs_with_letter(s, genre=genre),
                        sort_by_sentiment(sp, sentiment))
                else:
                    cache[s] = get_songs_with_letter(s, genre=genre)

            while True:
                # take the next element from the given iterator
                # if that fails, we tried all the songs already
                # and have nothing left to try
                try:
                    song = next(cache[s])
                except StopIteration:
                    break
                    # raise ValueError(
                    #    'Did not find a song for character {}'.format(s))

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


def get_sentiment(text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username=ibm['u'],
        password=ibm['p'],
        version="2017-02-27")

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            emotion=EmotionOptions(document=True),
            sentiment=SentimentOptions(document=True)))

    return {
        # => valence
        'positivity': (response["sentiment"]["document"]["score"] + 1) / 2,
        # => loundness
        'anger': -60 * response["emotion"]["document"]["emotion"]["anger"],
        # => danceability
        'joy': response["emotion"]["document"]["emotion"]["joy"],
        # => bpm
        'fear': 200 * response["emotion"]["document"]["emotion"]["fear"],
        # => acoustincess
        'sadness': response["emotion"]["document"]["emotion"]["sadness"]
    }


def sort_by_sentiment(sp, sentiment):
    print(sentiment)

    def sort(items):
        features = sp.audio_features(map(lambda t: t['id'], items))
        joined = zip(features, items)

        joined = sorted(joined, key=lambda fi: abs(
            sentiment['anger'] - (fi[0]['loudness'])))
        joined = sorted(joined, key=lambda fi: abs(
            sentiment['joy'] - fi[0]['danceability']))
        joined = sorted(joined,
                        key=lambda fi: abs(sentiment['fear'] - fi[0]['tempo']))
        joined = sorted(joined, key=lambda fi: abs(
            sentiment['sadness'] - fi[0]['acousticness']))
        joined = sorted(joined, key=lambda fi: abs(
            sentiment['positivity'] - fi[0]['valence']))

        result = map(lambda fi: fi[1], joined)
        print(list(joined)[0][0])
        return result

    return sort
