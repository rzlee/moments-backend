from flask import render_template, redirect, flash
from app import app
from forms import DeleteForm, LoginForm, EditForm
from models import Post

#----------------------------------------
# views 
#----------------------------------------

admin_key = "admin"

# views 
@app.route("/")
def index():
	user = {'name':'demodude'}
	return render_template("index.html", title = "moments", user = user)

@app.route("/all")
def all_posts():
	posts_found = Post.objects()
	posts = [{"imageurl":"a"}, {"imageurl":"b"}]
	return render_template("all.html", posts=posts_found)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
	form = DeleteForm()
	if form.key.data == admin_key:
		p = Post.objects(slug = form.slug.data)
		if len(p) == 1:
			#do stuff
			p = p[0]
			p.delete()
		else:
			raise Exception('Database Integrity Error')

	return render_template('delete.html', form = form)

@app.route("/edit", methods = ['GET', 'POST'])
def edit():
	form = EditForm()		
	if form.key.data == admin_key:
		#change the title
		p = Post.objects(slug = form.slug.data)
		if len(p) == 1:
			#do stuff
			p = p[0]
			p.title = form.title.data
			p.save()

	return render_template('edit.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()

	if form.key.data == admin_key: 
		return redirect('/')

	return render_template('login.html', form = form)
