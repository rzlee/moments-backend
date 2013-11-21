import os
from flask import Flask
import datetime

# initialization
app = Flask(__name__)
app.config.update(
    DEBUG = True,
)
app.config["SECRET_KEY"] = '\xf4\x9elyC\x10\xb3\xb4\xa8lhQ\xee}\xed\xd6\xdc\xd0vw\x896\x83\xc7'

#----------------------------------------
# database
#----------------------------------------

from mongoengine import connect
from flask.ext.mongoengine import MongoEngine

DB_NAME = 'testmoments'
DB_USERNAME = 'raj'
DB_PASSWORD = 'samplepassword'
DB_HOST_ADDRESS = 'ds053788.mongolab.com:53788/testmoments'

app.config["MONGODB_DB"] = DB_NAME
connect(DB_NAME, host='mongodb://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST_ADDRESS)
db = MongoEngine(app)

#----------------------------------------
# models
#----------------------------------------

# post model
class Post(db.DynamicDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)

    def __unicode__(self):
        return self.title

    @property
    def post_type(self):
        return self.__class__.__name__

    meta = {
        'allow_inheritance': True,
        'indexes': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }

# image model
class Image(Post):
    image_url = db.StringField(required=True, max_length=255)

# Get a post from db
def get_post_from_db(slug):
    if not slug:
        raise ValueError()
    posts_found = Post.objects(slug=slug)
    if len(posts_found) == 1:
        return posts_found[0]
    elif len(posts_found) == 0:
        return None
    else:
        raise Exception('Database Integrity Error')

#----------------------------------------
# controllers
#----------------------------------------

# controllers
@app.route("/")
def hello():
    post = get_post_from_db('testslug')
    if post is None:
        post = Post()
        post.slug = 'testslug'
        post.title = 'ttt'
        post.save()
    return "Hello from Python!"


# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
