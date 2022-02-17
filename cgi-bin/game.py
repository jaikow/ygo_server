#!./.venv/bin/python
from gevent import monkey
monkey.patch_all()


import os, sys, gc

PRELOAD = bool(os.environ.get('PRELOAD', 'True'))
if PRELOAD:
    gc.disable() # disabling the gc asap so we dont have empty spaces triggering COW on forks later on

sys.path.append("..")

from pathlib import Path
from typing import Dict


from flask import Flask, request, Blueprint
from flask_restx import Api, Resource
from loguru import logger
from lib.gunicorn_runner import FlaskApplication

os.environ['prometheus_multiproc_dir'] = os.environ.get('prometheus_multiplroc_dir', '/tmp/')
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics



ENV = os.environ.get('YGO_ENV', 'dev').lower()
PORT = os.environ.get('YGO_PORT', 7777)

app = Flask(__name__, static_url_path='/static')
GunicornInternalPrometheusMetrics(app)

api_bp = Blueprint('api', __name__)

api = Api(api_bp, default_label='YGO Server API')
app.register_blueprint(api_bp, url_prefix='/api')

app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/')
@app.route('/favicon.ico')
def favicon():
    return {}

@api.route('/health')
class GetHealth(Resource):
    def get(self):
        return 200


@app.errorhandler(Exception)
def internal_error(exception: Exception):
    ''' generic error handler '''
    msg = repr(exception)
    logger.opt(exception=True).error(msg)
    return { 'error': msg }, getattr(exception, 'code', 500)



if __name__ == '__main__':
    sys.argv = sys.argv[:1] # cleaning sysargs to not leak to gunicorn
    FlaskApplication(app, port=PORT, preload=PRELOAD).run()
