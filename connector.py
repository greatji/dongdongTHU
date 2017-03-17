# -*- coding:utf-8 -*-
# from sqlalchemy.orm import *
# from sqlalchemy import create_engine
from pymongo import MongoClient, ASCENDING
from appConfig import app

# engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
# MySql = sessionmaker(bind=engine)

Mongo = MongoClient('123.207.153.209', 27017)['test']
Mongo.authenticate("ubuntu", "ubuntu@2016")