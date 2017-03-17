# -*- coding:utf-8 -*-

import flask
from flask import Flask
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = '2016*platform'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=50)
# app.config['JWT_AUTH_URL_RULE'] = None
# app.config['JWT_AUTH_EMAIL_KEY'] = "email"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://ubuntu:ubuntu@2016@123.207.153.209:3306/platform?charset=utf8'
app.permanent_session_lifetime = timedelta(minutes=30)

# CORS(app)

# @app.route('/index', methods = ['GET'])
# def hello():
#     return flask.render_template('index.html')

def initialize():
    print 'init'