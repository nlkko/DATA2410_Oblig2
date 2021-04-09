from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import uuid

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

users = [
    {'id': "d45581f3a63f4b0b", 'username': 'Fire'},
    {'id': "f41cda46ec974d9e", 'username': 'Omelas'},
    {'id': "5a93949a308b4570", 'username': 'Dhalgren'}
]


@app.route('/api/users', methods=['GET', 'POST'])
def usr():
    # Returns all registered users in json
    if request.method == 'GET':
        return jsonify(users)
    
    # Registers an user
    if request.method == 'POST':
        new_user = {"id": uuid.uuid4().hex[:16], "username": request.json["username"]}
        users.append(new_user)
        return jsonify(users)


@app.route('/api/user/<string:user_id>', methods=['GET', 'DELETE'])
def usr_id(user_id):
    # Checks if selected id exists, if not throws an exception
    selected_user = None
    for user in users:
        if user["id"] == user_id:
            selected_user = user

    if selected_user is None:
        abort(404)

    # Return user with specific id
    if request.method == 'GET':
        return selected_user

    # Delete user with specific id
    if request.method == 'DELETE':
        users.remove(selected_user)
        return jsonify(users)


app.run()
