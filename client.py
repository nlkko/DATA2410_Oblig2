import threading
from flask import Flask, request, jsonify
import requests
import sys
import time

api_url = sys.argv[1]
user_id = "d45581f3a63f4b0b"
room_id = None
running = True


def commands(msg):
    global user_id
    global room_id

    if msg[0] != "/":
        return

    command = msg.split(' ')

    # Get a list of all commands
    if command[0] == "/help":
        return

    # Register as an user
    elif command[0] == "/register":  # <username>
        return

    # Login as a user
    elif command[0] == "/login":  # <user_id>
        user_id = msg[1]
        server_users = get_all_users()
        if server_users.status_code == 404:
            user_id = None
            return "Invalid user id"
        elif server_users.status_code == 400:
            return "No provided user id"
        elif server_users.status_code == 200:
            return ""
        else:
            return "An unexpected error occurred"

    # Join a room as a registered user
    elif command[0] == "/join":  # <room_id>
        try:
            req = requests.get("{}/api/room/{}".format(api_url, command[1]), json={"user_id": user_id})
            room_id = req.json()["id"]
            receive_thread = threading.Thread(target=receive_message)
            receive_thread.start()
            print("Changed room to {}".format(get_room(command[1])["name"]))

        except:
            print("\nSyntax or room_id is not valid. Type /help for more info")
            if req.status_code == 404:
                print("Room does not exist")
            elif req.status_code == 400:
                print("No provided user id")

    # Create a room
    elif command[0] == "/create":  # <room_name>
        req = requests.post("{}/api/rooms".format(api_url), json={"user_id": user_id, "name": command[1]})
        print(command[1] +" "+ req.json()["id"])
        print("Created a room with name: {} and id: {}".format(command[1], req.json()["id"]))
        

    else:
        print("Command does not exist")

def send_message():
    global running
    try:
        while running:
            msg = input("Write a message: \n")

            if msg[0] == "/":
                commands(msg)
            else:
                requests.post("{}/api/room/{}/{}/messages".format(api_url, room_id, user_id),
                              json={"user_id": user_id, "message": msg})
    except IndexError:
        print("Message can not be empty")
        threading.Thread(target=send_message).start()
    except EOFError:
        print("Program closed")
        running = False

def get_room(wanted_room_id):
    return requests.get("{}/api/room/{}".format(api_url, wanted_room_id), json={"user_id": user_id}).json()

def get_user(wanted_user_id):
    return requests.get("{}/api/user/{}".format(api_url, wanted_user_id), json={"user_id": user_id}).json()

def get_all_users():
    return requests.get("{}/api/users".format(api_url), json={"user_id": user_id})

def receive_message():
    global running
    try:
        old_message_array = []

        while running:
            # Finner bare de nye meldingene
            new_message_array = requests.get("{}/api/room/{}/messages".format(api_url, room_id),
                                             json={"user_id": user_id}).json()
            new_messages = new_message_array[(len(old_message_array)):]
            old_message_array = new_message_array
            time.sleep(0.5)

            if new_messages:
                for msg in new_messages:
                    print(get_user(msg["user_id"])["username"] + ": " + msg["message"])
    except:
        running = False
        print("send_thread stopped")


def start():
    print("Hello, welcome to wRESTling Bots Chat service")
    print("For access login with user id or create a user")
    print("Type /help for info")
    print()
    print()
    inp = None
    try:
        inp = input("Ignore for now\n")
        commands(inp)
    except:
        print("Program stopped")

    send_thread = threading.Thread(target=send_message)
    send_thread.start()


if __name__ == "__main__":
    start()
