import nltk
nltk.download('punkt')
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import requests
from io import StringIO
import pandas as pd


def emolexgram_main(text):

    """
      Takes text and adds if to a dictionary with 10 Keys  for each of the 10 emotions in the NRC Emotion Lexicon,
      each dictionary contains the value of the text in that emotions divided to the text word count
      INPUT: string
      OUTPUT: dictionary with the text and the value of 10 emotions
    """

    response = requests.get('https://raw.githubusercontent.com/mary123mary/EmoLexGram/master/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt')
    nrc = StringIO(response.text)



    emolecgram_dict = {'text': text, 'anger': [], 'anticipation': [], 'disgust': [], 'fear': [], 'joy': [], 'negative': [],
                  'positive': [], 'sadness': [], 'surprise': [], 'trust': []}

    emolecgram_df = pd.read_csv(nrc,
                            names=["word", "emotion", "association"],
                            sep=r'\t', engine='python')

    emolecgram_words = emolecgram_df.pivot(index='word',
                                   columns='emotion',
                                   values='association').reset_index()
    emolecgram_words.drop(emolecgram_words.index[0])

    emotions = emolecgram_words.columns.drop('word')

    stemmer = SnowballStemmer("english")

    document = word_tokenize(text)

    word_count = len(document)
    rows_list = []
    for word in document:
        word = stemmer.stem(word.lower())

        emo_score = (emolecgram_words[emolecgram_words.word == word])
        rows_list.append(emo_score)

    df = pd.concat(rows_list)
    df.reset_index(drop=True)

    for emotion in list(emotions):
        emolecgram_dict[emotion] = df[emotion].sum() / word_count

    return emolecgram_dict
