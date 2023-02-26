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
    
# def progress_chat_stage():

# def talk_about_movie_logic():


def maximum_context_switch_and_problem_space_reduction_algorithm(input):
    msg_vibe = sia.polarity_scores(input)
    if msg_vibe['neu'] > .3:
        return "Cool. Btw, I just watched " + random.choice(CORPUS["movie_titles"]) + ", have you seen it? Soooo good."
    # Redirect a particularly negative message
    if msg_vibe['neg'] > .8:
        "Wow. Anyways, have you seen " + random.choice(CORPUS["movie_titles"]) + "? That always cheers me up."
    # Redirect a particularly positive message
    if msg_vibe['pos'] > .6:
        "Wow, that's awesome! Reminds me of " + random.choice(CORPUS["movie_titles"]) + ". Badass flick."

class chat(actor):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.score = 0
        self.convo_state = actor.state
        self.salty_scale =  "MEDIUM"

    def get_output(self,msg_input):
        # still in greeting phase, exchange pleasantries
        if "init" == self.convo_state:
            for greeting_phrase in CORPUS["input_greetings"]:
                if greeting_phrase in nltk.word_tokenize(msg_input):
                    msg = random.choice(CORPUS["output_greetings"])
                    # We've got our greeting, exit loop
                    break
            # If we get this far, user has started a topic, be an ass and redirect to our own interest
            msg = maximum_context_switch_and_problem_space_reduction_algorithm(msg_input)
            # We have progressed the state of the conversation, and forced them to talk about movies
            self.convo_state = "movies"
            return msg
        # else if "movies" == self.convo_state
            # TODO Jarrett 
            # for movie in movieJSON:
                #     if movie in nltk.word_tokenize(msg_input):
                #         talk_about_movie_logic(movie)
        #Default
        # else

        sent = sia.polarity_scores(msg_input)

        if sent['neu'] > .3:
           self.salty_scale =  "MEDIUM"
        if sent['neg'] > .4:
            self.salty_scale =  "SALTY"
        if sent['pos'] > .6:
            self.salty_scale =  "SWEET"

        # Tag parts of speech from user message
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
