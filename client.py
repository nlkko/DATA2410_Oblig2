import threading
import requests
import sys
import time

api_url = sys.argv[1]
user_id = None
room_id = None
running = True
old_message_array = []
first_time_thread = 0


def commands(msg):
    global user_id
    global room_id
    global old_message_array
    global first_time_thread

    if msg[0] != "/":
        return

    command = msg.split(' ')

    # Get a list of all commands
    if command[0] == "/help":
        return ("""
            /help - provides info of all commands
            /register <username> - Registers a user
            /login <user_id> - Login as a user
            /join <room_id> - Join a specific room with room_id
            /create <room_name> - Create a room with the given name
            /delete_user <user_id> - Deletes user with given user_id, has to be user
            /delete_room <room_id> - Deletes room with giver room_id, has to be room creator
            /get_rooms - Get all rooms
            /get_room_users <room_id> - Get all users in a specific room (That you are in)
            """)

    # Register as an user
    elif command[0] == "/register":
        request = requests.post("{}/api/users".format(api_url), json={"username": command[1]})
        if request.status_code == 200:
            user_id = request.json()["id"]
            return "Registration successful \nYour user/login id is {}".format(user_id)
        else:
            return "An unexpected error occurred"

    # Login as a user
    elif command[0] == "/login":  # <user_id>
        try:
            user_id = command[1]
            request = get_user(user_id)
        except IndexError:
            return "No user id provided"

        if request.status_code == 404:
            user_id = None
            return "Invalid user id"
        elif request.status_code == 400:
            user_id = None
            return "No user id provided"
        elif request.status_code == 200:
            return "Login successful"
        else:
            user_id = None
            return "An unexpected error occurred"

    elif user_id is not None:

        # Join a room as a registered user
        if command[0] == "/join":  # <room_id>
            req = None
            try:
                req = requests.get("{}/api/room/{}".format(api_url, command[1]), json={"user_id": user_id})
                room_id = req.json()["id"]
                old_message_array = []
                if first_time_thread == 0:
                    first_time_thread = 1
                    receive_thread = threading.Thread(target=receive_message)
                    receive_thread.start()
                return "Changed room to {}".format(get_room(command[1]).json()["name"])

            except:
                print("\nSyntax or room_id is not valid. Type /help for more info")
                if req.status_code == 404:
                    return "Room does not exist"
                elif req.status_code == 400:
                    return "No provided user id"

        # Create a room
        elif command[0] == "/create":  # <room_name>
            req = requests.post("{}/api/rooms".format(api_url), json={"user_id": user_id, "name": command[1]})
            return "Created a room with name: {} and id: {}".format(command[1], req.json()["id"])

        # Delete user
        elif command[0] == "/delete_user":
            request = requests.delete("{}/api/user/{}".format(api_url, command[1]), json={"user_id": user_id})
            if request.status_code == 401:
                return "You are not permitted to delete this user"
            elif request.status_code == 200:
                return "Deletion successful and you have been logged out"

        # Delete room
        elif command[0] == "/delete_room":
            request = requests.delete("{}/api/room/{}".format(api_url, command[1]), json={"user_id": user_id})
            if request.status_code == 401:
                return "You are not permitted to delete this room"
            elif request.status_code == 200:
                user_id = None
                return "Deletion successful"

        # Gets rooms
        elif command[0] == "/get_rooms":
            return_string = ""
            for room in get_all_rooms().json():
                return_string += "id: {}   name: {}".format(room["id"], room["name"])
            return return_string

        # Gets all users in a room
        elif command[0] == "/get_room_users":  # <room_id>
            return_string = ""
            for user in get_all_room_users(command[1]).json():
                return_string += ("id: {}\n".format(user))
            return return_string

    else:
        return "Command does not exist"


def get_room(wanted_room_id):
    return requests.get("{}/api/room/{}".format(api_url, wanted_room_id), json={"user_id": user_id})


def get_user(wanted_user_id):
    return requests.get("{}/api/user/{}".format(api_url, wanted_user_id), json={"user_id": user_id})


def get_all_users():
    return requests.get("{}/api/users".format(api_url), json={"user_id": user_id})


def get_all_rooms():
    return requests.get("{}/api/rooms".format(api_url), json={"user_id": user_id})


def get_all_room_users(wanted_room_id):
    return requests.get("{}/api/room/{}/users".format(api_url, wanted_room_id), json={"user_id": user_id})


# def get_all_room_messages(wanted_room_id):
#    return requests.get("{}/api/room/{}/messages".format(api_url, wanted_room_id), json={"user_id": user_id})


def send_message():
    global running
    try:
        while running:
            msg = input("Write a message or command: \n")

            if msg[0] == "/":
                print(commands(msg))
            else:
                requests.post("{}/api/room/{}/{}/messages".format(api_url, room_id, user_id),
                              json={"user_id": user_id, "message": msg})
    except IndexError:
        print("Message can not be empty")
        threading.Thread(target=send_message).start()
    except EOFError:
        print("Program closed")
        running = False


def receive_message():
    global running
    global old_message_array
    old_message_array = []

    try:

        while running:
            # Finner bare de nye meldingene
            new_message_array = requests.get("{}/api/room/{}/messages".format(api_url, room_id),
                                             json={"user_id": user_id}).json()
            new_messages = new_message_array[(len(old_message_array)):]
            old_message_array = new_message_array
            time.sleep(0.5)

            if new_messages:
                for msg in new_messages:
                    print(get_user(msg["user_id"]).json()["username"] + ": " + msg["message"])
    except:
        running = False
        print("receive_thread stopped")


def start():
    print("Hello, welcome to wRESTling Bots Chat service")
    print("For access login with user id or create a user")
    print("Type /help for info")
    send_thread = threading.Thread(target=send_message)
    send_thread.start()


if __name__ == "__main__":
    start()
