import os
from flask import Flask, request, redirect, url_for
from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('config')

#----------------------------------------
# files
#----------------------------------------

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#----------------------------------------
# database
#----------------------------------------

DB_NAME = 'testmoments'
DB_USERNAME = 'raj'
DB_PASSWORD = 'samplepassword'
DB_HOST_ADDRESS = 'ds053788.mongolab.com:53788/testmoments'
app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

from app import views, models
