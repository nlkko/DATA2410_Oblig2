from flask import Flask, request, jsonify
from flask_restful import Api, abort
import uuid
import json

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

# Reading the JSON files
with open('users.json', encoding='utf-8') as f:
    users = json.load(f)

with open('rooms.json', encoding='utf-8') as f:
    rooms = json.load(f)


def write_json(obj, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(obj, f)


# Checks if given id exists then returns the object, if not throws an exception
def return_selected(search, objects, search_type="id"):
    selected = None
    for obj in objects:
        if obj[search_type] == search:
            selected = obj

    if selected is None:
        abort(404)

    return selected


# Users
@app.route('/api/users', methods=['GET', 'POST'])
def usr():
    # Returns all registered users in json
    if request.method == 'GET':
        # Checks if logged in user is valid
        try:
            logged_in_user = return_selected(request.json["user_id"], users)
        except TypeError:
            abort(404)
        except KeyError:
            abort(400)
        return jsonify(users)

    # Registers an user
    if request.method == 'POST':
        new_user = {"id": uuid.uuid4().hex[:16], "username": request.json["username"]}
        users.append(new_user)
        write_json(users, "users.json")
        return jsonify(new_user)


# Chat-Rooms:
@app.route('/api/user/<string:user_id>', methods=['GET', 'DELETE'])
def usr_id(user_id):
    selected_user = None
    logged_in_user = None
    # Checks if selected id exists, if not throws an exception
    try:
        selected_user = return_selected(user_id, users)
        logged_in_user = return_selected(request.json["user_id"], users)["id"]
    except TypeError:
        abort(404)
    except KeyError:
        abort(400)

    # Return user with specific id
    if request.method == 'GET':
        return selected_user

    # Delete user with specific id
    if request.method == 'DELETE':
        # Only a user can delete its user
        if logged_in_user != selected_user:
            abort(401)

        users.remove(selected_user)
        write_json(users, "users.json")
        return jsonify(users)


@app.route('/api/rooms', methods=['GET', 'POST'])
def roo():
    logged_in_user = None
    # Checks if logged in
    try:
        logged_in_user = return_selected(request.json["user_id"], users)["id"]
    except TypeError:
        abort(404)
    except KeyError:
        abort(400)

    # Returns all rooms in json
    if request.method == 'GET':
        return jsonify(rooms)

    # Creates a new room
    if request.method == 'POST':
        name = None
        try:
            name = request.json["name"]
        except KeyError:
            abort(400)
        new_room = {"id": uuid.uuid4().hex[:16], "name": name, "user_id": logged_in_user, "messages": [], "users": []}
        new_room["users"].append(logged_in_user)
        rooms.append(new_room)
        write_json(rooms, "rooms.json")
        return jsonify(new_room)


@app.route("/api/rooms/<string:user_id>", methods=['GET'])
def roo_us(user_id):
    # Checks if logged in
    try:
        logged_in_user = return_selected(request.json["user_id"], users)["id"]
    except TypeError:
        abort(404)
    except KeyError:
        abort(400)

    # Returns all rooms the user is part in
    rooms_with_user = []
    for room in rooms:
        if user_id in room["users"]:
            rooms_with_user.append(room)

    return jsonify(rooms_with_user)


@app.route("/api/room/<string:room_id>", methods=["GET", "DELETE"])
def roo_id(room_id):
    # Checks if logged in
    try:
        logged_in_user = return_selected(request.json["user_id"], users)
    except TypeError:
        abort(404)
    except KeyError:
        abort(400)

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
            write_json(rooms, "rooms.json")
            return jsonify(rooms)
        else:
            abort(401)


# Room users:
@app.route("/api/room/<string:room_id>/users", methods=['GET', 'POST'])
def roo_usrs(room_id):
    logged_user_id = None
    selected_room = None
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
        if logged_user_id not in selected_room["users"]:
            selected_room["users"].append(logged_user_id)
            write_json(rooms, "rooms.json")

        return jsonify(selected_room["users"])


# Messages for a room
@app.route("/api/room/<string:room_id>/messages", methods=["GET"])
def mess(room_id):
    selected_room = None
    logged_user_id = None
    # Checks if valid room and user
    try:
        selected_room = return_selected(room_id, rooms)
        logged_user_id = return_selected(request.json["user_id"], users)["id"]
    except TypeError:
        abort(404)
    except KeyError:
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
    selected_room = None
    requesting_user = None
    selected_user = None

    # Checks if user is valid
    try:
        selected_room = return_selected(room_id, rooms)
        selected_user = return_selected(user_id, users)["id"]
        requesting_user = return_selected(request.json["user_id"], users)["id"]
    except TypeError:
        abort(404)
    except KeyError:
        abort(400)

    # Checks if user is in room
    user_in_room = False
    for user in selected_room["users"]:
        if user == selected_user:
            user_in_room = True
            break
    # Checks if requesting user is in room
    requesting_in_room = False
    for user in selected_room["users"]:
        if user == requesting_user:
            requesting_in_room = True
            break

    if not user_in_room or not requesting_in_room:
        abort(401)

    # Sends all messages from specified user
    if request.method == "GET":
        user_messages = []
        for message in selected_room["messages"]:
            if message["user_id"] == user_id:
                user_messages.append(message)
        return jsonify(user_messages)

    # Post message from user
    if request.method == "POST":
        # Checks if posting user is the user it posts to
        if requesting_user != user_id:
            abort(401)

        in_message = None
        try:
            in_message = request.json["message"]
        except KeyError:
            abort(400)
        # Checks if message is empty
        if in_message == "":
            abort(406)

        # Adds message to room
        message = {"user_id": user_id, "message": in_message}
        selected_room["messages"].append(message)
        write_json(rooms, "rooms.json")
        return jsonify(message)


app.run()
