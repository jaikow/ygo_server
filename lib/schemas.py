''' Can be a message sent by Player or UI to the server containing an action (attack, flip, move, etc)
    Can also be a message being broadcast from the server containing an event (state, chain status, etc)
    All messages include an unique message ID for debugging
    This schema does not validate the msg contents inherently '''
msg_schema = {
    "type": "object",
    "properties": {
        "msg_type": {"type": "string"}, # message type, can be a player/UI action or something broadcast by the server
        "msg_ID": {"type": "string"},
        "content": {  # message content, follows a schema depending on the type of the message
            "type": "object",
        }
    },
    "required": ["msg_type", "msg_ID", "content"]
}


# INCOMING MESSAGES (FROM UNITY TO SERVER)

incoming_msg_types = ['start_game', 'change_phase', 'attack', 
                      'flip', 'move', 'pass', 'change_setting'
                      'play_card', 'activate', 'activation_choice',
                      'shuffle_hand']


''' UI sends the message to start a new game with all the player info
   This schema does not validate the board object inherently '''
start_game_schema = {
    "type": "object",
    "properties": {
        "player1_info": {
            "type": "object",
            "properties": {"hp": {"type": "integer"}, "board": {"type": "object"}},
            "required": ["hp", "board"]
        },
        "player2_info": {
            "type": "object",
            "properties": {"hp": {"type": "integer"}, "board": {"type": "object"}},
            "required": ["hp", "board"]
        }
    },
    "required": [ "player1_info", "player2_info"]
}

''' Player decides to change phase e.g. Main Phase 1 to Battle Phase '''
''' Can also be sent by the UI for changes of semiphases within a phase (e.g. Battle Phase' Battle Step to Damage Step)'''
''' Or by the server to the UI if any effects skips to a phase or semiphase immediately'''
change_phase_schema = {
    "type": "object",
    "properties": {
        "next_phase": {"type": "string"}
    },
    "required": ["next_phase"]
}

# serves to ensure correct phase progression. 
phase_specific_order = ["Start Phase", "Standby Phase", "Main Phase 1", "Battle Phase", "Main Phase 2", "End Phase"]

# Note that we are not going to validate this battlephase semiphase progression because I'm lazy
semiphase_specific_order = ["Start Step", "Battle Step", "Damage Step", "End Step"]

# parts of the Damage Step... why is yugioh like that :) also not going to validate this
semsemiphase_specific_oder = ["Before Damage Calculation", "During Damage Calculation", "After Damage Calculation"]

''' Player sends the message that one of his monsters will attack another card  '''

attack_schema = {
    "type": "object",
    "properties": {
        "attacker": {"type": "string"}, # cardID of the card that is attacking
        "receiver": {"type": "string"} # cardID of the card being attacked
    },
    "required": ["attacker", "receiver"]
}

''' Player sends the message that one of his monsters will attack another card  '''
flip_schema = {
    "type": "object", 
    "properties": {
        "which": {"type": "string"}, # cardID of the card that is being flipped
    },
    "required": ["which"]
}

move_schema = {
    "type": "object", 
    "properties": {
        "which": {"type": "string"}, # cardID of the card that is being moved from
        "to": {"type": "object"} # position that the card is being moved to
    },
    "required": ["which", "to"]
}

''' Player passing to finish a chain. 
    Note that chains can end without this message if the setting "End chains automatically" is enabled 
    if there is no valid play anymore from any players'''
pass_schema = {
    "type": "object",
    "properties": {
        "player": {"type": "string"}, # player sending the pass msg
    },
    "required": ["player"]
}

''' This message is sent when the player changes a game setting which affects how the board automation works'''
change_setting = {
    "type": "object",
    "properties": {
        "name": {"type": "string"}, # name of the setting being changed
        "new_value": {"type": "string"}
    },
    "required": ["name", "new_value"]
}

''' Is sent when the player plays a card from hand '''
play_card_schema = {
    "type": "object",
    "properties": {
        "which": {"type": "string"}, # cardID of the card  being played
        "where_to": {"type": "string"} # position that the card is being played at the field
    },
    "required": ["which", "which_to"]
}

''' Is sent when the player activates an effect of a monster '''
activate_schema = {
    "type": "object",
    "properties": {
        "which": {"type": "string"}, # cardID of the card whose effect is being activated
        "effect": {"type": "string"} # which effect of the card is being activated 
    },
    "required": ["which", "v"]
}

''' Player sends the message that they would like to shuffle their hand'''
shuffle_hand = {
    "type": "object",
    "properties": {
        "player": {"type": "string"}, # player sending the shuffle msg
    },
    "required": ["player"]
}



''' Note that the position object is validated later on, and not at Message creation time '''
position_schema = {
    "type": "object", 
    "properties": {
        "x": {"type": "integer"},
        "y": {"type": "integer"}
    },
    "required": ["x", "y"]
}


''' Player sends the message to pass i.e. you want to end that skill chain '''



# OUTGOING MESSAGES (BROADCAST FROM SERVER TO UNITY)


outgoing_msg_types = ['state', 'choose', 'negated', 'chain', 'legendary']


''' State of the whole game being broadcast from server to UI every time any one of these 'whats' changes '''
''' We can send the whole board state or just the deltas '''
state_schema = {
    "type": "object",
    "properties": {
        "state": {"type": "object"},
        "delta": {"type": "boolean"} # determines if the message is streaming only the delta of the state or full state 
    },
    "required": ["state", "delta"]
}

state_whats = ['deck', 'hand', 'graveyard', 'banished', 'hp', 'field', 'extra', 'side']

''' Message containing the state of a new/current chain happening in the game '''
''' We can send the whole chain state or just the deltas (new effects on the chain) '''
chain_schema = {
    "type": "object",
    "properties": {
        "what": {"chain": "object"},
        "delta": {"type": "boolean"} # same as state_schema
    },
    "required": ["chain", "delta"]
}

''' Message sent by server to UI whenever an effect was negated for any reason '''
negated_schema = {
    "type": "object",
    "properties": {
       "why": { # object with the cancelled card's cardID and specific effect that negated the effect
            "type": "object",
            "properties": {"card": {"type": "string"}, "effect_str": {"type": "string"}},
            "required": ["card", "effect_str"]
        } 
    },
    "required": ["why"]
}


''' Legendary message is the server broadcasting to the UI that the next state being sent will have to be dealt with on an
    unique manner e.g. time-reversal (UI needs to perform the interpret the deltas as reversals and play the reversed animations) '''
legendary_schema = {
    "type": "object",
    "properties": {
        "what": {"type": "string"}
    },
    "required": ["what"]
}



''' choose is a somewhat misleading name, since it also concerns dice rolls and coin tosses.
   Server signals the UI that the player needs to select a card, toss a coin or roll a dice
   The result of that will be sent by the UI to the server in the activation_choice message '''
choose_schema = {
    "type": "object",
    "properties": {
        "type_": {"type": "string"}, # can be "target", "roll", "toss"
        "valid_choices": { # if type_ is "target", this the list of cards (cardIDs) that an be targeted
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["type_", "valid_choices"]
}


activation_choice_schema = {
    "type": "object",
    "properties": {
        "choice": { # enlisted cardIDs of the selected cards if type_ was "target", enlisted rolled/tossed value if not
            "type": "array",
            "items": {
                "type": "string"
            }
        } 
    },
    "required": ["choice"]
}



''' This message is sent to signal the player to choose the order of effects that are playing simultaneously 
    He will then choose then in a LIFO manner i.e. the first he chooses is the last to run
    His choice will be sent back composing of a list of numbers on chain_choice_response_schema msg '''
chain_choice_request_schema = {
    "type": "object",
    "properties": {
        "valid_choices": { # list of cards (cardIDs) in which a player can choose the order of effects in chain
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": ["type_", "valid_choices"]
}


chain_choice_response_schema = {
    "type": "object",
    "properties": {
        "choice": {
            "type": "array",
            "items": {
                "type": "number"
            }
        } 
    },
    "required": ["value"]
}
