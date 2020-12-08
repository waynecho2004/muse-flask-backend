from flask import Flask, g
from flask_cors import CORS

from resources.songs import song

import models

# wcho: set to False in prodution
DEBUG = True 
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

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

# register blueprint: in order to use the song blueprint in songs.py
app.register_blueprint(song, url_prefix='/api/v1/songs')

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():        
    return "Welcome to Songs App"

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()   
    app.run(debug=DEBUG, port=PORT)    