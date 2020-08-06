from functools import wraps
import os, sys
import secrets
from functools import wraps
from PIL import Image
from flask import render_template, url_for, flash, abort, request, jsonify, make_response, session, redirect
from imagenflask import app
from imagenflask import forms,render,models
import json
from imagenflask.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from imagenflask.render import execute2, execute3
#from imagenflask.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_login import LoginManager
import pyrebase



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

#init firebase
firebase = pyrebase.initialize_app(config)
#Authenticate
auth=firebase.auth()
#real time database instance
db = firebase.database()
#real time storage instance
storage = firebase.storage()

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

#decorator to protect routes
def isAuthenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #check for the variable that pyrebase creates
        if not auth.current_user != None:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

#LOGIN system

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"] 
        try:
            # Log the user in
            user=auth.sign_in_with_email_and_password(email, password)
            #set the session
            user_id = user['idToken']
            user_email = email
            session['usr'] = user_id
            session["email"] = user_email
            flash('Logged In Successfully!', 'success')
            print("Successfully Logged In")
            return redirect(url_for('account')) 
        except:   
            print("Login Unsuccessful.")
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#REGISTRATION system

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if request.method == "POST":
        #get the request form data
        username = request.form["username"]
        affiliation = request.form["affiliation"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        data={
            "username": username, "affiliation": affiliation, "email": email
        }
        if password==confirm_password:
            try:
                #create the user
                auth.create_user_with_email_and_password(email, password)
                #auth.send_email_verification(user['idToken'])
                #login the user right away
                user = auth.sign_in_with_email_and_password(email, password)
                # Pass the user's idToken to the push method
                db.child("users").child(username).set(data, user['idToken'])
                #session
                

                
                
                return redirect("account.html",title='Account', form=form)
            except:
                return render_template("login.html", message="The email is already taken, try another one, please", form=form, title='Login' )  

    return render_template("register.html", title='Register', form=form)    
                

                # data to save
                #data = {
                #    "affiliation": 'affiliation', "email": 'email' 
                #}
                # Pass the user's idToken to the push method
                #db.child("users").child(username).set(data, user['idToken'])
                #return redirect(url_for('account')) 
            #except:
                #flash("The email already exists!", "danger") 
                #return render_template(url_for('login'))
        #else:
            #flash("Passwords do not match", "danger")  

    #return render_template('register.html', title='Register', form='form')

    #if request.method == "POST":
      #get the request form data
      #email = request.form["email"]
      #password = request.form["password"]
      #try:
        #create the user
        #auth.create_user_with_email_and_password(email, password);
        #login the user right away
        #user = auth.sign_in_with_email_and_password(email, password)   
        #session
        #user_id = user['idToken']
        #user_email = email
        #session['usr'] = user_id
        #session["email"] = user_email
        #return redirect("/") 
     # except:
      #  return render_template("login.html", message="The email is already taken, try another one, please" )  

    #return render_template("signup.html")

    #try:
    #    print(session['usr'])
    #    return redirect(url_for('admin'))
    #except KeyError:
    #    if request.method == "POST":
    #        email = request.form["login_email"]
    #        password = request.form["login_password"]
    #        try:
    #            user = auth.sign_in_with_email_and_password(email, password)
    #            user = auth.refresh(user['refreshToken'])
    #            user_id = user['idToken']
    #            session['usr'] = user_id
    #            return redirect(url_for('admin'))
    #        except:
    #            message = "Incorrect Password!"
    #    return render_template("login.html", message=message)


#LOGOUT system

@app.route("/logout")
def logout():
    #remove the token setting the user to None
    auth.current_user = None
    #also remove the session
    #session['usr'] = ""
    #session["email"] = ""
    session.clear()
    print("You have been signed out")
    flash('You have been signed out', 'success')
    return redirect(url_for('home'))

#PROFILE PIC aquisition System

def save_picture(form_picture):
    #Aquiring Location of the file
    filename=form_picture.filename
    #Setting Location on Firebase
    random_hex = secrets.token_hex(8)
    picture_path = os.path.join('profile_pics/', idToken)
    #Resizing File into required Dimensions
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    cloudfilename=picture_path
    #Uploading File onto cloud
    storage.child(cloudfilename).put(filename)
    return filename


@app.route("/account", methods=['GET', 'POST'])
# Import database module.
#from firebase_admin import rdb
@isAuthenticated
def account():
    # Get a database reference to our posts
    #ref = rdb.reference('server/saving-data/fireblog/posts')
    # Read the data at the posts reference (this is a blocking operation)
    #print(ref.get())
    form = UpdateAccountForm()
    user = db.child("users").get(session['usr']).val()
    print(user) #returns an Ordered Dictionary. Data needs to be extracted
    if request.method == 'POST':
        try:
            if form.picture.filename!="default.jpg":
                picture_file = save_picture(form.picture.data)
                user.image= picture_file
            form.username = user.username
            form.affiliation = user.affiliation
            form.email = user.email
            data = {
                "affiliation": user.affiliation, "email": user.email
            }
            # How to update a existing data
            db.child("users").child(current_user.username).update(data)
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
        except:
            flash('Username/Email already exists!', 'danger')

    return render_template('account.html', title='Account', form=form)


#POSTING on Blog

@app.route("/post/new", methods=['GET', 'POST'])
@isAuthenticated
def new_post():
    form = PostForm()
    if request.method == "POST":
        #get the request data
        title = request.form["title"]
        content = request.form["content"]

        post = {
          "title": title,
          "content": content,
          "author": session["username"]
        }

        try:
          #print(title, content, file=sys.stderr)
          #push the post object to the database
          db.child("Posts").child(session["username"]).push(post)
          return redirect(url_for('blog'), form=form)
        except:
          return render_template("create_post.html", message= "An error happened", form=form)  

    return render_template("create_post.html", title='New Post', form=form)

#form = PostForm()
 #   if form.validate_on_submit():
 #       post = Post(title=form.title.data, content=form.content.data, author=current_user)
 ##       db.child("users").child(current_user.username).append(post, user['idToken'])
  #      flash('Your post has been created!', 'success')
  ##      return redirect(url_for('blog'))
   # return render_template('create_post.html', title='New Post',
   #                        form=form, legend='New Post')



#@app.route("/post/<int:post_id>")
#def post(post_id):
#    post = Post.query.get_or_404(post_id)
#    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<id>")
@isAuthenticated
def post(id):
    orderedDict = db.child("Posts").order_by_key().equal_to(id).limit_to_first(1).get()
    print(orderedDict, file=sys.stderr)
        
    return render_template("post.html", data=orderedDict, title=post.title)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@isAuthenticated
def update_post(post_id):
    form = PostForm()
    if post.author != current_user:
        abort(403)
    if request.method == "POST":

          title = request.form["title"]
          content = request.form["content"]

          post = {
            "title": title,
            "content": content,
            "author": session["email"]
          }

          #update the post
          db.child("Posts").child(id).update(post)
          return redirect("/post/" + id) 

    orderedDict =  db.child("Posts").order_by_key().equal_to(id).limit_to_first(1).get()
    return render_template("edit.html", data=orderedDict, title='Update Post', form=form)


    #post = Post.query.get_or_404(post_id)
    #if post.author != current_user:
    #    abort(403)
    #form = PostForm()
    #if form.validate_on_submit():
    #    post.title = form.title.data
    #    post.content = form.content.data
    #    db.session.commit()
    #    flash('Your post has been updated!', 'success')
    #    return redirect(url_for('post', post_id=post.id))
    #elif request.method == 'GET':
    #    form.title.data = post.title
    #    form.content.data = post.content
    #return render_template('create_post.html', title='Update Post',
     #                      form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@isAuthenticated
def delete_post(post_id):
    db.child("Posts").child(id).remove()
    return redirect("/")

    #post = Post.query.get_or_404(post_id)
    #if post.author != current_user:
    #    abort(403)
    #db.session.delete(post)
    #db.session.commit()
    #flash('Your post has been deleted!', 'success')
    #return redirect(url_for('home'))



@app.route("/data")
@isAuthenticated
def data():
    return render_template('data.html', title='Data')

@app.route("/blog")
def blog():
    posts = db.child('posts').get()
    if posts.val() == None:
        return render_template('blog.html', title='Blog')
    else:    
        return render_template('blog.html', posts=posts, title='Blog')

@app.route("/res")
def res():
    return render_template('res.html', title='Resources')

@app.route("/forum")
def forum():
    browser = request.user_agent.browser
    uas = request.user_agent.string
    if (browser == 'firefox') :
        return render_template('forum.html')
    return render_template('forumupdated.html', title='Forum')

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

