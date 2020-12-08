import models
from flask import Blueprint, jsonify, request

# playhouse.shortcuts (from peewee) is a module contains helper 
# functions for expressing things that would otherwise be somewhat 
# verbose or cumbersome using peewee’s APIs. There are also helpers 
# for serializing models to dictionaries and vice-versa.
from playhouse.shortcuts import model_to_dict

# first argument is blueprints name  (songs.py)
# second argument is it's import_name
song = Blueprint('songs', 'song')
## Example using the blueprint:  
##    @song.route('/'):
##        Add views to song blueprint using the route decorator

## INDEX ROUTE
# Add views to song blueprint using the route decorator
@song.route('/', methods=["GET"])   
def get_all_songs():
    ## find the songs and change each one to a dictionary into a new array
    try:
        songs = [model_to_dict(song) for song in models.Song.select()]
        print(songs)  # logging
        return jsonify(data=songs, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

## SHOW ROUTE
@song.route('/<id>', methods=["GET"])
def get_one_song(id):
    try:
        print(id, 'reserved word?')
        song = models.Song.get_by_id(id)
        print(song.__dict__)
        return jsonify(data=model_to_dict(song), status={"code": 200, "message": "Success"})  
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

## POST ROUTE
@song.route('/', methods=["POST"])
def create_songs():
    ## see request payload anagolous to req.body in express
    try:
        payload = request.get_json()
        print(type(payload), 'payload')
        song = models.Song.create(**payload)
        ## see the object
        print(song.__dict__)
        ## Look at all the methods
        print(dir(song))
        # Change the model to a dict
        print(model_to_dict(song), 'model to dict')
        song_dict = model_to_dict(song)
        return jsonify(data=song_dict, status={"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error creating a song"})

## UPDATE ROUTE
@song.route('/<id>', methods=["PUT"])
def update_song(id):
    try:
        payload = request.get_json()
        # update will update the selected fields, e.g. (artist)
        query = models.Song.update(**payload).where(models.Song.id==id)  
        query.execute()
        return jsonify(data=model_to_dict(models.Song.get_by_id(id)), status={"code": 200, "message": "resource updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error updating a song"})

## DELETE
@song.route('/<id>', methods=["Delete"])
def delete_song(id):
    try:
        query = models.Song.delete().where(models.Song.id==id)
        query.execute()
        return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})    
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error deleting a song"})        