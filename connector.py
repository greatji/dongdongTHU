# -*- coding:utf-8 -*-
# from sqlalchemy.orm import *
# from sqlalchemy import create_engine
from pymongo import MongoClient, ASCENDING
from appConfig import app
import redis

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
# MySql = sessionmaker(bind=engine)

Mongo = MongoClient('123.207.155.225', 27017)['test']
Mongo.authenticate("ubuntu", "dongdong1.2.3.!")
Redis = redis.Redis()