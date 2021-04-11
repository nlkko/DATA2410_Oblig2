import threading
from flask import Flask, request, jsonify
import requests
import sys
import time

api_url = sys.argv[1]
user = None

def recieve_message:
    try:
        while True:
            return

            time.sleep(0.5)
    return

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

def send_message:
    msg = input("Write a message: ")

    if msg[0] == "/":
        commands(msg)
    return