import yaml
from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from os.path import exists

from tools.logging import logger
from util.chat import chat

import pickle

yml_configs = {}
BODY_MSGS = []
with open('config.yml', 'r') as yml_file:
    yml_configs = yaml.safe_load(yml_file)

CORPUS = {}

def fetch_history(from_number):
    act = None
    #Check if phone number has saved history
    if exists( f"users/{from_number}.pkl") :
        with open(f"users/{from_number}.pkl", 'rb') as p:
            act = pickle.load(p)
    else:
        #If no history, start recording
        act= chat(from_number)
    return act

def handle_request():
    logger.debug(request.form)

    act = fetch_history(request.form['From'])

    act.save_msg(request.form['Body'])
    output = act.get_output(request.form['Body'])

    for o_msg in output:
         message = g.sms_client.messages.create(
                     body=o_msg,
                     from_=yml_configs['twillio']['phone_number'],
                     to=request.form['From'])

    with open(f"users/{request.form['From']}.pkl", 'wb') as p:
         pickle.dump( act, p)

    return json_response( status = "ok" )




