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



class chat(actor):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.score = 0
        self.convo_state = "init"
        self.salty_scale =  "MEDIUM"
    
    def memorize_movie(self, title):
        self.current_movie = title
    
    def recall_movie(self):
        return self.current_movie
    
    def reference_movie(self, tokenized_input):
        msg_vibe = sia.polarity_scores(tokenized_input)
        if msg_vibe['pos'] > .6:
            msg_vibe = "positive"
        # If they weren't enthusiastic, they hated it, and they hate you.
        else:
            msg_vibe = "negative"
        
        movie_title = self.recall_movie()

        # Accessing JSON object properties in Python is fun!
        msg = random.choice(CORPUS["reference_movie"][movie_title][msg_vibe])
        return msg
    
    def maximum_context_switch_and_problem_space_reduction_algorithm(self, input):
        msg_vibe = sia.polarity_scores(input)
        random_movie = random.choice(CORPUS["movie_titles"])
        if msg_vibe['neu'] > .3:
            output = "Cool. Btw, I just watched " + random_movie + ", have you seen it? Soooo good."
        # Redirect a particularly negative message
        if msg_vibe['neg'] > .5:
            output = "Wow. Anyways, have you seen " + random_movie + "? That always cheers me up."
        # Redirect a particularly positive message
        if msg_vibe['pos'] > .5:
            output = "Woah, that's awesome! Reminds me of " + random_movie + ". Badass flick."
        
        # Remember this movie for future reference    
        self.memorize_movie(random_movie)
        return output
    
    def get_output(self,msg_input):
        # still in greeting phase, exchange pleasantries
        print("Convo state:" + self.convo_state)
        # Convert to lowercase, tokenize
        tokenized_input = nltk.word_tokenize(msg_input.lower())
        print(tokenized_input)
        if "init" == self.convo_state:
            for greeting_phrase in CORPUS["input_greetings"]:
                if greeting_phrase in tokenized_input:
                    msg = random.choice(CORPUS["output_greetings"])
                    # We've got our greeting, return it
                    return msg
            # If we get this far, user has started a topic, be an ass and redirect to our own interest
            msg = self.maximum_context_switch_and_problem_space_reduction_algorithm(msg_input)
            # We have progressed the state of the conversation, and forced them to talk about movies
            self.convo_state = "movies"
            return msg
        elif "movies" == self.convo_state:
            # We've initiated talking about our movie, steamroll the conversation
            msg = random.choice

            # Respond to user asking about ~any movie
            # for movie in CORPUS:
                    # if movie in nltk.word_tokenize(msg_input):
                        # talk_about_movie_logic(movie)
        #Default
        else:

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
            for i in range( len(CORPUS[ "misc" ]) ):
                msg = random.choice( CORPUS[ "misc" ] )
                if msg not in self.prev_msgs:
                    break

            if msg == None:
                return [ random.choice( CORPUS[ "misc" ] ) ]
            else:
                return [ msg ]
