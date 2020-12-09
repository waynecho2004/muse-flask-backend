from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

import models

# importing resources
from resources.songs import song
from resources.user import user

# sets up the ability to set up the session
login_manager = LoginManager()

# wcho: set to False in prodution
DEBUG = True 
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

######### Add Following lines ######
## Need secrete_key to encode the session
app.secret_key = "LJAKLJLKJJLJKLSDJLKJASD" 
# set up the sessions on the app
login_manager.init_app(app) 
# A decorator function, which will load the user object whenever we access the session, 
# we can get the user by importing current_user from the flask_login
@login_manager.user_loader 

def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

# Add Cors support
CORS(song, origins=['http://localhost:3000'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000'], supports_credentials=True)

# register blueprint: in order to use the 
#   song blueprint from songs.py and user blueprint from user.py
app.register_blueprint(song, url_prefix='/api/v1/songs')
app.register_blueprint(user, url_prefix='/user')

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():        
    return "Welcome to Songs App"

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)    