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
        if msg_vibe['pos'] > .4:
            msg_vibe = "positive"
        # If they weren't enthusiastic, they hated it, and they hate you.
        else:
            msg_vibe = "negative"
        
        movie_title = self.recall_movie()

        print("Current movie topic: " + movie_title)
        print("Message vibe: " + msg_vibe)
        # Accessing JSON object properties in Python is fun!
        movies = CORPUS["reference_movie"]
        movie = movies[movie_title]
        print("Possible lines:")
        for line in movie[msg_vibe]:
            print(line)
        
        msg = None
        for i in len(movie[msg_vibe]):
            potential_msg = random.choice(movie[msg_vibe])
            if potential_msg not in self.prev_msgs:
                msg = potential_msg
                break

        if msg == None:
            self.panic_mode()
        else:
            return [ msg ]
        
        # msg = random.choice(CORPUS["reference_movie"][movie_title][msg_vibe])
        return msg
    
    def get_random_movie(self):
        return random.choice(CORPUS["movie_titles"])

    def maximum_context_switch_and_problem_space_reduction_algorithm(self, input):
        msg_vibe = sia.polarity_scores(input)
        random_movie = self.get_random_movie()
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
    
    def handle_convo_init(self, msg_input):
        for greeting_phrase in CORPUS["input_greetings"]:
                if greeting_phrase in msg_input:
                    msg = random.choice(CORPUS["output_greetings"])
                    # We've got our greeting, return it
                    self.convo_state = "smalltalk"
                    return msg
        # If we get this far, user has started a topic, be an ass and redirect to our own interest
        msg = self.maximum_context_switch_and_problem_space_reduction_algorithm(msg_input)
        # We have progressed the state of the conversation, and forced them to talk about movies
        self.convo_state = "movies"
        return msg
    
    def panic_mode(self):
        # We've run out of things to say, spam movie lines I guess?
        for i in range( len(CORPUS[ "misc" ]) ):
            msg = random.choice( CORPUS[ "misc" ] )
            if msg not in self.prev_msgs:
                break

        if msg == None:
            return [ random.choice( CORPUS[ "misc" ] ) ]
        else:
            return [ msg ]

    def handle_convo_smalltalk(self, msg_input):
        for phrase in CORPUS["input_smalltalk_a"]:
            if phrase in msg_input:
                msg = "Good, what about you?"
                return msg
        for phrase in CORPUS["input_smalltalk_b"]:
            if phrase in msg_input:
                msg = "Not much, what have you been up to?"
                return msg
            
        # If they said something we haven't accounted for
        movie_title = self.get_random_movie()
        if "who" or "what" or "when" or "where" or "why" or "how" or "?" in msg_input:
            self.memorize_movie(movie_title)
            # We have progressed the state of the conversation, and forced them to talk about movies
            self.convo_state = "movies"
            return "Honestly dude, I don't even know right now. I just watched " + movie_title + " again, you seen it?"
        else:
            # They went way off the rails
            return self.panic_mode()

    def get_output(self,msg_input):
        # still in greeting phase, exchange pleasantries
        print("Convo state:" + self.convo_state)
        # Convert to lowercase
        msg_input = msg_input.lower()
        # tokenized_input = nltk.word_tokenize(msg_input.lower())
        # print(tokenized_input)

        # Ears perk up
        for trigger in CORPUS["movie_triggers"]:
            if trigger in msg_input:
                if "init" == self.convo_state:
                    msg = self.maximum_context_switch_and_problem_space_reduction_algorithm(msg_input)
                    self.convo_state = "movies"
                    return msg
                else:
                    self.convo_state = "movies"

        if "init" == self.convo_state:
            return self.handle_convo_init(msg_input)
        elif "smalltalk" == self.convo_state:
            return self.handle_convo_smalltalk(msg_input)
        elif "movies" == self.convo_state:
            # We've initiated talking about our movie, steamroll the conversation
            msg = self.reference_movie(msg_input)
            return msg

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
