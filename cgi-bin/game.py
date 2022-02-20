#!/bin/sh
"exec" "`dirname $0`/../.venv/bin/python" "$0" "$@"

import os, sys
ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(ROOT, '..'))

import json

from werkzeug.debug import DebuggedApplication
from flask import Flask, request, Blueprint
from flask_restx import Api, Resource as FlaskResource
from geventwebsocket import WebSocketServer, Resource

from loguru import logger

from lib.aux_methods import find_free_port
from lib.game_state import GameStateApplication


ENV = os.environ.get('YGO_ENV', 'dev').lower()
PORT = 7777 if ENV == 'dev'else find_free_port()

app = Flask(__name__, static_url_path='/static')

api_bp = Blueprint('api', __name__)

api = Api(api_bp, default_label='YGO Server API')
app.register_blueprint(api_bp, url_prefix='/api')

app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/')
@app.route('/favicon.ico')
def favicon():
    return {}

@app.errorhandler(Exception)
def internal_error(exception: Exception):
    ''' generic error handler '''
    msg = repr(exception)
    logger.opt(exception=True).error(msg)
    return { 'error': msg }, getattr(exception, 'code', 500)


@api.route("/websocket")
class WebSocketDocs(FlaskResource):
    '''Describes the websocket API documentation'''
    def get(self):
        return {}

@api.route('/health')
class GetHealth(FlaskResource):
    def get(self):
        return 200

@api.route('/loadgame')
class LoadGame(FlaskResource):
    ''' Gamestate will be saved constantly (run info on UI and current game info on this serve)'''
    ''' This endpoint loads and returns the pickled game info (board state) for the player to continue a game '''
    def get(self):
        return 200


if __name__ == '__main__':
    logger.info(f"Serving on port {PORT}")
    WebSocketServer(('0.0.0.0', PORT),
                    Resource([('^/game', GameStateApplication),
                              ('^/.*', DebuggedApplication(app))
                             ]),
                    debug=False).serve_forever()
