import os, gc
from gunicorn.app.base import Application
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics
from flask_restx import api
from flask import url_for


def child_exit(_, worker):
    ''' exit hook for metrics '''
    GunicornInternalPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)

def when_ready(server):
    # this makes it so objects creted before server startup are all immortal
    # i.e. they wont be refcounted by gc, so reads on them wont trigger ref-count writes
    # which in turn wont trigger Copy-on-Write
    gc.freeze()

def post_fork(server, worker):
    gc.enable()


class FlaskApplication(Application):
    ''' class to wrap gunicorn setup '''

    def __init__(self, app, local_port, preload, num_workers=17, **kwargs):
        self.app = app
        self.local_port = local_port
        self.num_workers = num_workers
        self.kwargs = kwargs
        self.preload = preload
        super().__init__()


    def init(self, parser, opts, args): # pylint:disable=W0613
        ''' sets custom config for gunicorn '''
        default_config = {'bind': f'{os.environ.get("HOST", "0.0.0.0")}:{self.local_port}',
                          'worker_tmp_dir': '/tmp/shm',
                          'workers': self.num_workers,
                          'timeout': 86400, 'child_exit': child_exit, 'loglevel': 'info',
                          'worker_class': 'gevent', 'preload_app': True}
        
        if self.preload:
            default_config.update({'when_ready': when_ready, 'post_fork': post_fork})

        return {**default_config, **self.kwargs}

    def load(self):
        return self.app