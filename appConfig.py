# -*- coding:utf-8 -*-

import flask
from flask import Flask
# from flask_cors import CORS
from datetime import datetime, timedelta
from celery import Celery

# CORS(app)

# @app.route('/index', methods = ['GET'])
# def hello():
#     return flask.render_template('index.html')


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
app = Flask(__name__)

app.config['SECRET_KEY'] = '2016*platform'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=50)
# app.config['JWT_AUTH_URL_RULE'] = None
# app.config['JWT_AUTH_EMAIL_KEY'] = "email"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://ubuntu:ubuntu@2016@123.207.153.209:3306/platform?charset=utf8'
app.permanent_session_lifetime = timedelta(minutes=30)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERYBEAT_SCHEDULE = {
        'sms': {
            'task': 'sms',
            'schedule': timedelta(minutes=5)
            # 'schedule': timedelta(seconds=10)
        },
    }
)
celery = make_celery(app)


# @celery.task()
# def add_together(a, b):
#     return a + b



from batch_notify import sms_task
@celery.task(name='sms')
def sms_periodic():
    sms_task()
    print 'done'

def initialize():
    print 'init'