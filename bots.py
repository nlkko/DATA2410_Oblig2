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
bot_name = None
in_room = False
bot_names = ["Bot_Tobias", "Bot_William", "Bot_Adrian", "Bot_Eirik"]

"""
phases:
user-phase # Create a new user or login
room-phase # Create a new room or join
message-phase # Send message to the different rooms
"""


def login(name, api_url):
    global bot_id
    global bot_name

    if name not in bot_names:
        return False

    request = requests.get("{}/api/users".format(api_url), json={"user_id": bot_id}).json()
    exist = False

    for user in request:
        if user["username"] == name:
            exist = True
            bot_id = user["id"]
            break

    bot_name = name

    if exist:
        return "/login " + bot_id
    else:
        return "/register " + bot_name


def join():
    return


def bot_message():
    global in_room
    global bot_name
    msg = None

    print(bot_name)
    if bot_name == "Bot_Tobias":
        return msg

    elif bot_name == "Bot_William":
        return msg

    elif bot_name == "Bot_Adrian":
        return msg

    elif bot_name == "Bot_Eirik":
        return msg

    else:
        return "Invalid bot name"

