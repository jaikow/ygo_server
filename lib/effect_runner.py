from lib import primitive_effects


class EffectRunner():
    ''' This class' purpose is to trigger a primitive effect and depending on its result broadcast a msg
        A chain is composed of a list of EffectRunners scheduled to be run in a LIFO order '''

    def __init__(self, effect_name, **kwargs):
        effect_result, details = getattr(primitive_effects, effect_name)(kwargs)

        if effect_result == 'Successful':
            pass # build board delta dict and broadcast it as state msg
        elif effect_result == 'Create chain':
            pass # build chain message and broadcast it. chain msg might be delta if details specify this
        elif effect_result == 'Negated':
            pass # build negated msg with details and broadcast it
