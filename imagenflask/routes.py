import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, abort, request, jsonify, make_response, session, redirect
from imagenflask import app, db, bcrypt
from imagenflask import forms,render,models
import json
from imagenflask.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from imagenflask.render import execute2, execute3
from imagenflask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



sums=0

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/data")
def data():
    return render_template('data.html', title='Data')

@app.route("/blog")
@login_required
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts, title='Blog')

@app.route("/res")
@login_required
def res():
    return render_template('res.html', title='Resources')

@app.route("/forum")
@login_required
def forum():
    return render_template('blog.html', posts=posts, title='Forum')

@app.route("/team")
def team():
    return render_template('team.html', title='Team')

@app.route("/process", methods=["POST"])
def process():
	print("process is called")
	if request.method == "POST":
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		#print(clicked)
		#print(type(clicked))
		first = clicked.split(";")[0]
		
		a=int(first)

		session['first'] = a

		sums = a
		print(type(sums))
		#print(type(sums))
		#def display(sums):
		print(sums)
		return json.dumps({"sum" : sums})

@app.route("/process1", methods=["POST"])
def process1():
	
	if request.method == "POST":
		print("process1 is called")
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		#print(clicked)
		#print(type(clicked))
		print(clicked)
		second = clicked.split(";")[0]
		b=int(second)
		#session['second'] = b
		copya=session['first']
		#session.pop('first', None)
		
		sums = render.execute2(copya, b)
		print(type(sums))
		#print(type(sums))
		#def display(sums):
		print(sums)
		session['secondsum'] = sums
		return json.dumps({"sum" : sums})

@app.route("/process2", methods=["POST"])
def process2():
	
	if request.method == "POST":
		print("process2 is called")
		clicked=request.form['data']
    	# sum=render.add(a,b,c)
		#print(clicked)
		#print(type(clicked))
		#first = clicked.split(";")[0]
		#second = clicked.split(";")[1]
		third = clicked.split(";")[0]
		print(type(third))
		c=int(third)
		print(type(c))
		d=session['secondsum']
		session.pop('first', None)
		session.pop('secondsum', None)

		sums = render.execute3(c,d)
		print(type(sums))
		print(sums)
		#console.log(sums)
		print(sums)
		return json.dumps({"sum" : sums})

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))



