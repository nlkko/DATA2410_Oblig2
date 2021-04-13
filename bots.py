import requests


"""
------ Krav til botene -----
○ Register as a user once
○ Join an existing room and create a new one
○ Post several messages in all the roms it's a part of and also fetch all
messages in those rooms. Great bots respond to other messages. Lesser
bots just post things. Both are welcome.
○ Implement a basic user interface for a human to observe and optionally
interact with the chat rooms. The user interface can be a simple terminal
program or a web page that lets the user select which of the actions
accessible in the API it wants to take (for example, fetch all messages from
room 42) and then asks for input to that action where applicable (for example,
if the action is to post a message to room 42, allow the user to type in the
message they want to send)
"""
bot_id = "admin"
in_user = False
in_room = False

"""
phases:
user-phase # Create a new user or login
room-phase # Create a new room or join
message-phase # Send message to the different rooms
"""

def login(bot_name):
    global in_user
    global bot_id

    r = requests.get("{}/api/users".format(api_url), json={"user_id": user_id}).json()
    exist = False

    for user in r:
        if user["username"] == bot_name:
            exist = True
            bot_id = user["id"]
            break
    
    in_user = True

    if exist:
        return "/login " + bot_id
    else:
        return "/register " + bot_name

def join():
    return

def bot_message(bot):
    global in_user
    global in_room

    if bot == "Bot_Tobias":
        # Will create a Bot_Tobias user if it doesn't exist, else will login to Bot_Tobias
        if not in_user:
            login(bot)

        # Will check all rooms the bot is in and join one

        return msg

    if bot == "Bot_William":
        return msg

    if bot == "Bot_Adrian":
        return msg

    if bot == "Bot_Eirik":
        return msg