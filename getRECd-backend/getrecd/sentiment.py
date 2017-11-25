import json
from credentials import ibm

from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, KeywordsOptions, EntitiesOptions, EmotionOptions, SentimentOptions

def getSentiment(text):
    natural_language_understanding = NaturalLanguageUnderstandingV1(
      username=ibm['u'],
      password=ibm['p'],
      version="2017-02-27")

    response = natural_language_understanding.analyze(
        text=text,
        features=Features(
            emotion=EmotionOptions(document=True),
            sentiment=SentimentOptions(document=True)))

    report = {}
    positivity = response["sentiment"]["document"]["score"] # Valence — The higher the value, the more positive mood for the song.
    positivity +=1
    report["positivity"] = positivity/2
    report["anger"] = response["emotion"]["document"]["emotion"]["anger"] # Loudness — The higher the value, the louder the song (in dB).
    report["joy"] = response["emotion"]["document"]["emotion"]["joy"] # Danceability — The higher the value, the easier it is to dance to this song.
    report["fear"] = response["emotion"]["document"]["emotion"]["fear"] # Beats Per Minute (BPM) — The tempo of the song.
    report["sadness"] = response["emotion"]["document"]["emotion"]["sadness"] # Acousticness — The higher the value the more acoustic the song is.
    print(report)
    return(report)

text = 'Why would Kim Jong-un insult me by calling me "old," when I would NEVER call him "short and fat?" Oh well, I try so hard to be his friend - and maybe someday that will happen!'
getSentiment(text)
