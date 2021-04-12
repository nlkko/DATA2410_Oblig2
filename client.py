import threading
from flask import Flask, request, jsonify
import requests
import sys
import time

api_url = sys.argv[1]
user_id = "d45581f3a63f4b0b"
room_id = "d45581f3a63f4b0a"

def commands(msg):
    command = msg.split(' ')
    # Get a list of all commands
    if command[0] == "/help":
        return

    # Register as an user
    elif command[0] == "/register": # <username>
        return

    # Login as a user
    elif command[0] == "/login": # <user_id>
        return
        
    # Join a room as a registered user
    elif command[0] =="/join": # <room_id>
        return

    # Create a room
    elif command[0] =="/create": # <room_name>
        return
        
    else:
        print("Command does not exist")

def send_message():
    try:
        while True:
            msg = input("Write a message: ")

            if msg[0] == "/":
                commands(msg)
            else:
                requests.post("{}/api/room/{}/{}/messages".format(api_url, room_id, user_id), json={"user_id": user_id, "message": msg})
    except:
        print("send_message ended")

def get_user(wanted_user_id):
    return requests.get("{}/api/user/{}".format(api_url, wanted_user_id), json={"user_id": user_id}).json()

def receive_message():
    try:
        new_message_array = []
        old_message_array = []

        while True:
            # Finner bare de nye meldingene
            new_message_array = requests.get("{}/api/room/{}/messages".format(api_url, room_id), json={"user_id": user_id}).json()
            new_messages = new_message_array[(len(old_message_array)):]
            old_message_array = new_message_array
            time.sleep(0.5)

            if new_message_array:
                for msg in new_messages:
                    print(get_user(msg["user_id"])["username"] +": " + msg["message"])
    except:
        print("send_thread stopped")

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()