import datetime
from app import db

#----------------------------------------
# models
#----------------------------------------

# post model
class Post(db.DynamicDocument):
	#created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	title = db.StringField(max_length=255, required=True)
	slug = db.StringField(max_length=255, required=True)
	# We have to use stringField here because Flask-MongoEngine does not support
	# GeoLocationField types
	geoLong = db.StringField(max_length=255, required=True)
	geoLat = db.StringField(max_length=255, required=True)
	image_url = db.StringField(required=True, max_length=255)

	@property
	def post_type(self):
		return self.__class__.__name__

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}
