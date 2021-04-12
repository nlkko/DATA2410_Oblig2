import threading
from flask import Flask, request, jsonify
import requests
import sys
import time

api_url = sys.argv[1]
user_id = None
room_id = "d45581f3a63f4b0a"
running = True


def commands(msg):
    global user_id

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
        return

    # Create a room
    elif command[0] == "/create":  # <room_name>
        return

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
    inp = None
    try:
        inp = input("Ignore for now\n")
        commands(inp)
    except:
        print("Program stopped")

    threading.Thread(target=receive_message).start()
    threading.Thread(target=send_message).start()


if __name__ == "__main__":
    start()
