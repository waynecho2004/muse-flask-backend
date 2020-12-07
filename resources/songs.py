import models
from flask import Blueprint, jsonify, request

# playhouse.shortcuts (from peewee) is a module contains helper 
# functions for expressing things that would otherwise be somewhat 
# verbose or cumbersome using peewee’s APIs. There are also helpers 
# for serializing models to dictionaries and vice-versa.
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name  (dogs.py)
# second argument is it's import_name
dog = Blueprint('songs', 'song')