from flask import Flask
from pyrebase import pyrebase
from flask_login import LoginManager

app = Flask(__name__)

#Initializing Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#SecretKey
app.config['SECRET_KEY'] = 'imageniitb_alankar'

from imagenflask import routes
