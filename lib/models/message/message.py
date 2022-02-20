import json
from jsonschema import validate
from lib.schemas import * # I agree that this is ugly and stinky, but so is importing each schema separatedly

class Message():
    ''' Generic Message Class, all messages will follow the same ctor '''

    def __init__(self, json_msg):
        ''' Sets every key from the message without restrictions, as properties for the object'''
        msg = json.loads(json_msg)
        content_validator = globals()[f'{msg["message_type"]}_schema']
        validate(msg, msg_schema)
        validate(msg['content'], content_validator)

        # if validation went well, set the properties dynamically on the json to this Message obj
        [setattr(self, key, value) for key,value in msg]