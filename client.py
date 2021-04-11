import threading
from flask import Flask, request, jsonify
import requests
import sys
import time

api_url = sys.argv[1]
user_id = None
room_id = None

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
        
        else:
            print("Command does not exist")
"""
def username_of_id(wanted_user_id):
    return requests.get(api_url +"/api/user/"+ wanted_user_id, data={"user_id: "+ user_id})["username"]

def send_message():
    try:
        while True:
            msg = input("Write a message: ")

            if msg[0] == "/":
                commands(msg)
    except:
        print("send_message ended")

def recieve_message():
    new_message_array = requests.get(api_url + "/api/room/"+ room_id +"/messages", data={"user_id: "+ user_id})
    old_message_array = []
    
    try:
        while True:
            new_messages = [msg for msg in new_message_array if msg not in old_message_array]
            old_message_array = new_message_array
            time.sleep(0.5)

            for msg in new_messages:
                print(username_of_id(msg["id"]) +": "+msg["message"])

    except:
        print("recieve_message ended")