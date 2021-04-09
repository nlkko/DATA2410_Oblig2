from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

from flask import request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

users = [
    {'id': 0, 'username': 'Fire'},
    {'id': 1, 'username': 'Omelas'},
    {'id': 2, 'username': 'Dhalgren'}
]

@app.route('/api/users', methods=['GET', 'SET'])
def usr():
    # Returns all registered users in json
    if request.method == 'GET':
        return jsonify(users)
    
    # Registers an user
    if request.method == 'SET':
        newUser = { "id": len(users), "username": request.args.get('username') }
        users.append(newUser)

        return jsonify(users)

"""
@app.route('/api/user/<user-id>', methods=['GET', 'SET'])
def usr_id():
    # Return user with specific id
    if request.method == 'GET':

    # Delete user with specific id
    return
"""
app.run()