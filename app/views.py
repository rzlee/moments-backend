import random
import os
import hashlib
from flask import render_template, redirect, flash, request, url_for, send_from_directory, jsonify
from app import app
from forms import DeleteForm, LoginForm, EditForm, UploadForm, GeoForm
from models import Post
from werkzeug import secure_filename

# allowed files
def allowed_file(filename):
	ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
	return '.' in filename and \
	   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

#----------------------------------------
# views 
#----------------------------------------

admin_key = "admin"

# views 
@app.route('/', methods=['GET', 'POST'])
def index():
	user = {'name':'joe bar'}
	form = UploadForm()
	return render_template("index.html", title = "moments", user = user, form = form)

@app.route('/all-list', methods=['GET', 'POST'])
def list_all():
	posts_found = Post.objects()
	return render_template("all.html", title = "moments", posts = posts_found)

counter = 0

@app.route('/upload', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			hash = hashlib.md5()
			hash.update(filename);
			global counter
			new_filename = str(hash.hexdigest()[14:]) + '_' + str(random.random()*100) + str(counter)
			hash.update(new_filename)
			counter = counter + 1
			filename = hash.hexdigest()[20:] + '_' + filename
			hashstring = str(hash.hexdigest()[20:])
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			print path
			file.save(path)
			url = url_for('uploaded_file', filename=filename)
			data = {
					"response" : "Success",
					"slug": hashstring,
					"image_url": url
					}
			return jsonify(data)

@app.route('/create', methods=['POST'])
def create():
	post = Post()
	post.title = request.args.get('title', '')
	post.slug = request.args.get('slug', '')
	post.geoLong = request.args.get('geoLong', '')
	post.geoLat = request.args.get('geoLat', '')
	post.image_url = request.args.get('image_url', '')
	post.save()
	data = {
			"response" : "Success",
			}
	return jsonify(data)

@app.route('/upload-combined', methods=['POST'])
def upload_file_combined():
	form = UploadForm()
	if request.method == 'POST':
		file = request.files['file']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			hash = hashlib.md5()
			hash.update(filename);
			global counter
			new_filename = str(hash.hexdigest()[14:]) + '_' + str(random.random()*100) + str(counter)
			hash.update(new_filename)
			counter = counter + 1
			filename = hash.hexdigest()[20:] + '_' + filename
			hashstring = str(hash.hexdigest()[20:])
			path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			print path
			file.save(path)
			url = url_for('uploaded_file', filename=filename)
			post = Post()
			post.title = form.title.data
			post.slug = hashstring
			post.geoLong = form.geoLong.data
			post.geoLat = form.geoLat.data
			post.image_url = url
			post.save()
			return redirect("/all-list")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/all")
def all_posts():
	posts_found = Post.objects()
	# return render_template("all.html", posts=posts_found)
	array = [];
	for post in posts_found:
		temp = {};
		temp["title"] = post.title
		temp["slug"] = post.slug
		temp["image_url"] = post.image_url
		temp["geoLong"] = post.geoLong
		temp["geoLat"] = post.geoLat
		array.append(temp);
	data = {"data":array}
	return jsonify(data)

@app.route('/delete', methods = ['GET', 'POST'])
def delete():
	form = DeleteForm()
	if form.key.data == admin_key:
		p = Post.objects(slug = form.slug.data)
		if len(p) >= 1:
			for post in p:
				post.delete()
		else:
			raise Exception('Database Integrity Error')

	return render_template('delete.html', form = form)

@app.route("/edit", methods = ['GET', 'POST'])
def edit():
	form = EditForm()		
	if form.key.data == admin_key:
		#change the title
		p = Post.objects(slug = form.slug.data)
		if len(p) >= 1:
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

@app.route('/tag', methods = ['GET', 'POST'])
def tag_image():
	if request.method == 'POST':
		slugval = str(request.form['slug'])
		tagval = str(request.form['tag'])
		print slugval
		p = Post.objects(slug = slugval)
		print len(p)
		if len(p) >= 1:
			#otherwise somethings wrong
			post = p[0]
			post.tags.append(tagval)
			post.save()
		tag_url = '/tagged/' + tagval
		return redirect(tag_url)
	posts_found = Post.objects()
	return render_template('tag.html', posts = posts_found)

@app.route('/tagged/<tagname>')
def list_tagged(tagname):
	posts_found = Post.objects(tags=tagname)
	return render_template("viewtag.html", title = "tagged", posts = posts_found, tag = tagname)

@app.route('/geo', methods = ['GET', 'POST'])
def geo_list():
    form = GeoForm()
    posts_found = []
    for post in Post.objects():
        if within_ran(post, form.lat.data, form.lon.data):
            posts_found.append(post)
    return render_template("geo.html", title = "geo", posts = posts_found, form = form)

def within_ran(post, lat, lon):
    ran = 0.0005
    if post == None or lat == None or lon == None:
        return False
    lat = float(lat)
    lon = float(lon)
    post_lat = float(post.geoLat)
    post_lon = float(post.geoLong)
    return (lat - ran <= post_lat and lat + ran >= post_lat) and (lon - ran <= post_lon and lon + ran >= post_lat)

@app.route('/about')
def about():
	return render_template("about.html")
