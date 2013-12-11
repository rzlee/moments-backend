from flask.ext.wtf import Form
from wtforms import TextField

class DeleteForm(Form):
	slug = TextField('slug')
	key = TextField('key')

class LoginForm(Form):
	key = TextField('key')

class EditForm(Form):
	slug = TextField('slug')	
	title = TextField('title')	
	key = TextField('key')	

class TaggedForm(Form):
	tag = TextField('tag')
