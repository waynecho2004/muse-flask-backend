import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash
from flask_login import login_user
from playhouse.shortcuts import model_to_dict # this is peewee playhouse package

# first argument is blueprints name
# second argument is it's import_name
user = Blueprint('users', 'user')

@user.route('/register', methods=["POST"])
def register():
    ## see request payload analogous to request.body in express
    ## This is how you get the image you sent over
    ## using .get_json() to retrieve the json from the route
    ## This has all the data like username, email, password
    payload = request.get_json()

    # convert email to lower case to be consistent
    payload['email'].lower()
    try:
        # Find if the user already exists?  
        # The model query finding user by email
        models.User.get(models.User.email == payload['email']) 
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})

    except models.DoesNotExist:
        # bcrypt line for generating the hash
        payload['password'] = generate_password_hash(payload['password']) 

        user = models.User.create(**payload) # put the user in the database
        # **payload, is spreading like js (...) the properties of the payload object out

        #login_user: start the session and log in
        login_user(user) 

        # Use model_to_dict in order to read the model. (The model is its own class)
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        # Best Practice: delete the password for security purpose
        del user_dict['password'] # delete the password before we return it, because we don't need the client to be aware of it
        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})


