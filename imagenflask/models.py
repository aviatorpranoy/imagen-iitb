from datetime import datetime
from imagenflask import login_manager
from flask_login import UserMixin
from flask_login import current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#class User(db):
    #id = db.Column(db.Integer, primary_key=True)
#    username = current_user.username
#    email = current_user.email
#    image_file = current_user.image_file
#    password = current_user.password
#    posts = current_user.posts

    #def __repr__(self):
    #    return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#class Post(db):
    #id = db.Column(db.Integer, primary_key=True)
    #title = current_user.title
    #date_posted = current_user.date_posted
    #content = current_user.content
    #user_id = current_user.user_id

    #def __repr__(self):
        #return f"Post('{self.title}', '{self.date_posted}')"