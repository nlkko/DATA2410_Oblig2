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

rooms = [
    {'id': "d45581f3a63f4b0a", "name": "Test", "creator_id": "d45581f3a63f4b0b"}
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
            break

    if selected_user is None:
        abort(404)

    # Return user with specific id
    if request.method == 'GET':
        return selected_user

    # Delete user with specific id
    if request.method == 'DELETE':
        users.remove(selected_user)
        return jsonify(users)


@app.route('/api/rooms', methods=['GET', 'POST'])
def roo():
    # Returns all rooms in json
    if request.method == 'GET':
        return jsonify(rooms)

    # Creates a new room
    if request.method == 'POST':
        new_room = {"id": uuid.uuid4().hex[:16], "name": "", "creator_id": ""}
        users.append(new_room)
        return jsonify(rooms)


@app.route("/api/room/<string:room_id>", methods=["GET", "DELETE"])
def roo_id(room_id):
    selected_room = None
    user_id = ""
    for room in rooms:
        if room["id"] == room_id:
            selected_room = room
            break

    # Room doesn't exist
    if selected_room is None:
        abort(404)

    # Returns room
    if request.method == "GET":
        return selected_room

    # Deletes room if user_id was the same as the room creator
    if request.method == "DELETE":
        if user_id == selected_room["creator_id"]:
            rooms.remove(selected_room)
            return jsonify(rooms)
        else:
            abort(400)


app.run()
