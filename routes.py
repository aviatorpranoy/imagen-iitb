import os, sys
import secrets
from PIL import Image
from imagenflask import db, bcrypt
from flask import render_template, url_for, flash, abort, request, jsonify, make_response, redirect, session
from imagenflask import app, mail
import json
from imagenflask import render, forms, models
from imagenflask.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from imagenflask.render import execute2, execute3
from imagenflask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
from collections import OrderedDict
#from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message
import pyrebase
import requests
import datetime
import random
import time
#from werkzeug import secure_filename

UPLOAD_FOLDER = 'static/image_upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


config ={
    "apiKey": "AIzaSyAjOG33EzmXwzjWn3emhH_jZW46kD0rINo",
    "authDomain": "imagentest-e48fa.firebaseapp.com",
    "databaseURL": "https://imagentest-e48fa.firebaseio.com",
    "projectId": "imagentest-e48fa",
    "storageBucket": "imagentest-e48fa.appspot.com",
    "messagingSenderId": "735866948920",
    "appId": "1:735866948920:web:f0b0770cd2d56c3443c5cd",
    "measurementId": "G-RYB1W48273"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

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


#LOGIN system

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        username=form.username.data
        affiliation=form.affiliation.data
        email=form.email.data
        password=form.password.data

        print(username, affiliation, email, password)
        user = auth.create_user_with_email_and_password(email, password)
        print(user)
        uid =  user['localId']
        data = {
                 "name": username,
                 "email" : email,
                 "affiliation" : affiliation,
                 "avatar": "default.jpg"
                
        }

        print( user)
        result = db.child("users").child(uid).set(data)

        return redirect(url_for('login'))






        
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password = form.password.data
        print(email, password)

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            print(user)
            session['login'] = True
            session['userID'] = user['localId']
            return redirect(url_for('account'))




        
        except requests.HTTPError as e:
            error_json = e.args[1]
            print(error_json)
            error = json.loads(error_json)['error']['message']
            print(error)
            if error == "EMAIL_EXISTS":
                print("Email already exists")
        
        


    return render_template('login.html', title='Login', form=form)


#LOGOUT system

@app.route("/logout")
def logout():
    #logout_user()
    session.pop('login', None)
    session.pop('userID', None)
    return redirect(url_for('home'))


#PROFILE PIC aquisition System

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

def account():
    if 'login' in session:

        
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.picture.data:

                print(form.picture.data)
                #filename = secure_filename(form.picture.data.filename)
                #form.picture.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #tmp = random.randint(100000,999999)
                picture_file = save_picture(form.picture.data)
                #time.sleep(10)
                
                #storage.child("profile_pics").put("static/profile_pics/"+picture_file)

                #path = os.path.abspath()

                storage.child("profile_pics/"+str(picture_file)).put("imagenflask/static/profile_pics/"+picture_file)
                


                image_url = "profile_pics/"+picture_file
                db.child("users").child(session['userID']).update({"avatar": image_url})
            else:
                image_url = "NA" 
                #current_user.image_file = picture_file
            username = form.username.data
            affiliation = form.affiliation.data
            email = form.email.data


            db.child("users").child(session['userID']).update({"name": username})
            db.child("users").child(session['userID']).update({"email": email})

            db.child("users").child(session['userID']).update({"affiliation": affiliation})
            



            #db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        elif request.method == 'GET':

            print(session['userID'])
            allPost = db.child("users").child(session['userID']).get()
            allP = (allPost.val())
            print(allP)
            allP = list(allP.items())
            print(allP)
            


            

            form.username.data = allP[3][1]
            form.affiliation.data = allP[0][1]
            form.email.data = allP[2][1]
 
            image_file = storage.child(allP[1][1]).get_url(None)
        
        return render_template('account.html', title='Account', form=form, image = image_file, loggedin=True)
    else:
        return redirect(url_for('login'))


#POSTING on Blog

@app.route("/post/new", methods=['GET', 'POST'])
#@login_required
def new_post():
    if 'login' in session:
        form = PostForm()
        print(session['login'], session['userID'])
        if form.validate_on_submit():
            title=form.title.data
            content=form.content.data
            #author=current_user
            x = datetime.datetime.now()
            x = x.strftime("%d-%m-%Y %H:%M:%S")

            tmp = (random.randint(100000000000000,999999999999999))
            tmp = str(tmp)
            
            data = {
                 "title": title ,
                 "content" : content,
                 "userID" : session['userID'],
                 "timestamp" : x,
                 "id" : tmp}
            

            
            result = db.child("blog").child(tmp).set(data)
            



            return redirect(url_for('blog'))
        return render_template('create_post.html', title='New Post',
                            form=form, legend='New Post', loggedin=True)
    else:
        return redirect(url_for('login'))



@app.route("/post/<int:post_id>")
def post(post_id):
    print(post_id)

    allPost = db.child("blog").child(post_id).get()
    allP = (allPost.val())
    allP = list(allP.items())
    print(allP)
    content = allP[0][1]
    postID = allP[1][1]
    timestamp = allP[2][1]
    title = allP[3][1]
    userID = allP[4][1]
    print(content) 
    #add username
    usersDetails = db.child("users").child(userID).get()
    u = usersDetails.val()
    allDetails = list(u.items())
    print(allDetails)
    name = (allDetails[3][1])
    affiliation = (allDetails[0][1])
    avatar = storage.child(allDetails[1][1]).get_url(None)
    email = (allDetails[2][1])
    #userDict = {'name' : name, 'affiliation' : affiliation, 'avatar' : avatar, 'email' : email}
    #singlePost.update(userDict)


    #post = Post.query.get_or_404(post_id)
    if 'login' in session:
        return render_template('post.html', loggedin=True, title=title, content = content, postID = postID, timestamp = timestamp, userID = userID, name=name, affiliation = affiliation, avatar = avatar, email = email)
    else:
        return render_template('post.html', loggedin=False, title=title, content = content, postID = postID, timestamp = timestamp, userID = userID, name=name, affiliation = affiliation, avatar = avatar, email = email)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def update_post(post_id):
    #post = Post.query.get_or_404(post_id)
    #if post.author != current_user:
    #    abort(403)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        '''
        data = {
                "blog/"+str(post_id): {
                    "title": title
                },
               "blog/"+str(post_id): {
                    "content" : content
                }
            }
        '''
        
        db.child("blog").child(post_id).update({"title": title})
        db.child("blog").child(post_id).update({"content": content})

            
        #db.update(data)




        #db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post_id))
    elif request.method == 'GET':
        allPost = db.child("blog").child(post_id).get()
        allP = (allPost.val())
        allP = list(allP.items())
        print(allP)
        content = allP[0][1]
        postID = allP[1][1]
        timestamp = allP[2][1]
        title = allP[3][1]
        userID = allP[4][1]
        print(content) 
        



        form.title.data = title
        form.content.data = content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post', loggedin=True)


@app.route("/post/<int:post_id>/delete", methods=['POST'])
def delete_post(post_id):
    
    db.child("blog").child(post_id).remove()

    #db.session.delete(post)
    #db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog'))



@app.route("/data")
def data():
    if 'login' in session:
        return render_template('data.html', title='Data',loggedin=True)
    else:
        return redirect(url_for('login'))

@app.route("/blog")
def blog():
    #page = request.args.get('page', 1, type=int)
    #posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    posts = []
    allPost = db.child("blog").get()
    for single in allPost.each():
        singlePost = single.val()
        print(singlePost)
        print(type(singlePost))

        #add username
        usersDetails = db.child("users").child(singlePost['userID']).get()
        u = usersDetails.val()
        allDetails = list(u.items())
        print(allDetails)
        name = (allDetails[3][1])
        affiliation = (allDetails[0][1])
        avatar = storage.child(allDetails[1][1]).get_url(None)
        email = (allDetails[2][1])
        userDict = {'name' : name, 'affiliation' : affiliation, 'avatar' : avatar, 'email' : email, 'date': singlePost['timestamp'].split(" ")[0]}
        singlePost.update(userDict)



        posts.append(singlePost)


    print(posts)
    #x = singlePost['timestamp']
    #posts.sort(key=lambda x: time.strptime(x, '%Y-%m-%d %H:%M:%S')[0:6], reverse=True)
    if 'login' in session:
        return render_template("blog.html", posts=posts, title='Blog',loggedin=True)
    else:
        return render_template("blog.html", posts=posts, title='Blog',loggedin=False)
#posts = db.child('posts').get()
#if posts.val() == None:
#return render_template('blog.html', title='Blog')
#else:    
#return render_template('blog.html', posts=posts, title='Blog')

@app.route("/res")
def res():
    if 'login' in session:
        return render_template('res.html', title='Resources',loggedin=True)
    else:
        return render_template('res.html', title='Resources',loggedin=False)

@app.route("/forum")
def forum():
    browser = request.user_agent.browser
    uas = request.user_agent.string
    if (browser == 'firefox') :
        if 'login' in session:
            return render_template('forum.html', loggedin=True)
        else:
            return render_template('forum.html', loggedin=False)
    else:
        if 'login' in session:
            return render_template('forumupdated.html', title='Forum',loggedin=True)
        else:
            return render_template('forumupdated.html', title='Forum',loggedin=False)

@app.route("/team")
def team():
    if 'login' in session:
        return render_template('team.html', title='Team',loggedin=True)
    else:
        return render_template('team.html', title='Team',loggedin=False)

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=10)
    if 'login' in session:
        return render_template('user_posts.html', posts=posts, user=user,loggedin=True)
    else:
        return render_template('user_posts.html', posts=posts, user=user,loggedin=False)     

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
The link is valid for 30mins only!
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)