import threading
from flask import Flask, request, jsonify
import requests
import sys
import time

api_url = sys.argv[1]
user_id = "d45581f3a63f4b0b"
room_id = "d45581f3a63f4b0a"

"""
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
"""
def username_of_id(wanted_user_id):
    return requests.get("{}/api/user/{}".format(api_url, wanted_user_id), json={"user_id ": user_id})["username"]

def send_message():
    try:
        while True:
            msg = input("Write a message: ")

            if msg[0] == "/":
                commands(msg)
    except:
        print("send_message ended")

def recieve_message():
    new_message_array = requests.get("{}/api/room/{}/messages".format(api_url, room_id), json={"user_id": user_id})
    old_message_array = []
    
    try:
        while True:
            # Finner bare de nye meldingene
            new_messages = [msg for msg in new_message_array if msg not in old_message_array]
            old_message_array = new_message_array
            time.sleep(0.5)

            for msg in new_messages:
                print(username_of_id(msg["id"]) +": "+msg["message"])

    except:
        print("recieve_message ended")

send_thread = threading.Thread(target= recieve_message)
send_thread.start()