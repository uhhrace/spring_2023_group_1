import json
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import random

from util.actors import actor

sia = SentimentIntensityAnalyzer()

CORPUS = {}
with open('chatbot_corpus.json', 'r') as myfile:
    CORPUS = json.loads(myfile.read())

def get_movie_title(movie_index):
    with open('util/tmdb_movies.json', 'r') as movie_list:
        movies_info = json.loads(movie_list.read())

        return movies_info[movie_index].get('title')

class chat(actor):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.score = 0

        self.salty_scale =  "MEDIUM"

    def get_output(self,msg_input):
        sent = sia.polarity_scores(msg_input)

        if sent['neu'] > .3:
           self.salty_scale =  "MEDIUM"
        if sent['neg'] > .4:
            self.salty_scale =  "SALTY"
        if sent['pos'] > .6:
            self.salty_scale =  "SWEET"

        pos_tags =  nltk.pos_tag( nltk.word_tokenize(msg_input))

        msg = None
        for i in range( len(CORPUS[ "misc corpus" ]) ):
            msg = random.choice( CORPUS[ "misc corpus" ] )
            if msg not in self.prev_msgs:
                break

        if msg == None:
            return [ random.choice( CORPUS[ "misc corpus" ] ) ]
        else:
            return [ msg ]





