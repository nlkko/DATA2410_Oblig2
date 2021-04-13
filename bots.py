import requests
import random
import uuid

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

def join(api_url):
    request = requests.get("{}/api/rooms".format(api_url), json={"user_id": bot_id}).json()
    rooms = []
    for room in request:
        rooms.append(room["id"])

    print(rooms)

    if random.random() <= 0.8:
        room = "/join "+ random.choice(rooms)
        print(room)
        return room
    else:
        return "/create " + uuid.uuid4().hex[:4]

def bot_message():
    global in_room
    global bot_name
    msg = "AAAAAA"

    if not in_room:
            in_room = True
            return join("http://127.0.0.1:5000/")

    print(bot_name)
    if bot_name == "Bot_Tobias":
        messages = [
            "樂高生化戰士 是樂高積木由",
            "故事載體在2003年時變為小說和漫畫兩種",
            "並由樂高的新系列《英雄工廠》",
            "년에 처음으로 만들어졌으며"
        ]

        msg = random.choice(messages)
        return msg

    elif bot_name == "Bot_William":
        messages = [
            "I used to ride a unicycle as a kid",
            "My favorite song is Bohemian rhapsody by Queen",
            "My hair is long and lushy, like olive oil",
            "As a kid my favorite show was Caillou"
        ]

        msg = random.choice(messages)
        return msg

    elif bot_name == "Bot_Adrian":
        return msg

    elif bot_name == "Bot_Eirik":
        return msg

    else:
        return "Invalid bot name"

