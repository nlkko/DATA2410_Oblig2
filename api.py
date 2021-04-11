from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort
import uuid
import requests

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

users = [
    {'id': "d45581f3a63f4b0b", 'username': 'Fire'},
    {'id': "f41cda46ec974d9e", 'username': 'Omelas'},
    {'id': "5a93949a308b4570", 'username': 'Dhalgren'}
]

rooms = [
    {'id': "d45581f3a63f4b0a",
     "name": "Test",
     "user_id": "d45581f3a63f4b0b",
     "users": ["d45581f3a63f4b0b", "f41cda46ec974d9e", "5a93949a308b4570"],
     "messages": [
         {
             "user_id": "5a93949a308b4570",
             "message": "Hey mister"
         },
         {
             "user_id": "f41cda46ec974d9e",
             "message": "Hey fister"
         }
     ]},
    {'id': "f41cda46ec974d9f",
     "name": "Test2",
     "user_id": "d45581f3a63f4b0b",
     "users": [""],
     "messages": [
         {
             "user_id": "d45581f3a63f4b0b",
             "message": "Hello"
         },
         {
             "user_id": "f41cda46ec974d9e",
             "message": "Hey there"
         }
     ]},
]


# Checks if given id exists then returns the object, if not throws an exception
def return_selected(id, objects, type="id"):
    selected = None
    for obj in objects:
        if obj[type] == id:
            selected = obj

    if selected is None:
        abort(404)

    return selected


# Users
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


# Chat-Rooms:
@app.route('/api/user/<string:user_id>', methods=['GET', 'DELETE'])
def usr_id(user_id):
    # Checks if selected id exists, if not throws an exception
    selected_user = return_selected(user_id, users)

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
        new_room = {"id": uuid.uuid4().hex[:16], "name": "", "user_id": ""}
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
        if user_id == selected_room["user_id"]:
            rooms.remove(selected_room)
            return jsonify(rooms)
        else:
            abort(401)


# Room users:
@app.route("/api/room/<string:room_id>/users", methods=['GET', 'POST'])
def roo_usrs(room_id):
    try:
        # Check if user_id is valid
        logged_user_id = return_selected(request.json["user_id"], users)["id"]
        selected_room = return_selected(room_id, rooms)
    except TypeError:
            # Handles exception if user does not give input an user_id
            abort(400)

    # Get all users from a room
    if request.method == 'GET':
        return jsonify(selected_room["users"])

    # Add a user to a room OBS: Only registered users can join
    if request.method == 'POST':
        # Checks if user is not already in the room
        if selected_user not in selected_room["users"]:
            selected_room["users"].append(selected_user)
        return jsonify(selected_room["users"])
        


# Messages for a room
@app.route("/api/room/<string:room_id>/messages", methods=["GET"])
def mess(room_id):
    try:
        selected_room = return_selected(room_id, rooms)
        logged_user_id = return_selected(request.json["user_id", users])["id"]
    except TypeError:
        abort(400)

    in_room = False
    # Checks if user that sent request is in room
    for use in selected_room["users"]:
        if use == logged_user_id:
            in_room = True
            break

    if not in_room:
        abort(401)

    # Returns messages
    if request.method == "GET":
        return jsonify(selected_room["messages"])


# Messages for one user in a room
@app.route("/api/room/<string:room_id>/<string:user_id>/messages", methods=["GET", "POST"])
def mess_user(room_id, user_id):
    selected_room = return_selected(room_id, rooms)

    # Checks if user is valid
    try:
        selected_user = return_selected(user_id, users)
    except:
        abort(404)

    # Checks if user is in room
    in_room = False
    for user in selected_room["users"]:
        if user == user_id:
            in_room = True
            break

    if not in_room:
        abort(404)

    # Sends all messages from specified user
    if request.method == "GET":
        user_messages = []
        for message in selected_room["messages"]:
            if message["user_id"] == user_id:
                user_messages.append(message)
        return jsonify(user_messages)

    # Post message from user
    if request.method == "POST":
        message = {"user_id": user_id, "message": ""}
        selected_room["messages"].append(message)
        return jsonify(message)


app.run()
