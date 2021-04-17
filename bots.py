import requests
import random
import uuid

bot_id = "admin"
url = None
bot_name = None
in_room = False
leave_chance = -1
exit_chance = -1
messages_sent = 0
total_messages_sent = 0
bot_names = ["Bot_Tobias", "Bot_William", "Bot_Adrian", "Bot_Eirik"]


def login(name, api_url):
    global bot_id
    global bot_name
    global url

    # Checks if the bot name exists 
    if name not in bot_names:
        return False

    request = requests.get("{}/api/users".format(api_url), json={"user_id": bot_id}).json()
    exist = False

    # Checks if the bot is registered
    for user in request:
        if user["username"] == name:
            exist = True
            bot_id = user["id"]
            break

    bot_name = name
    url = api_url
    if exist:
        return "/login " + bot_id
    else:
        # If its not registered it will create a user with its name
        return "/register " + bot_name


def join():
    global in_room
    # Gets all rooms
    request = requests.get("{}/api/rooms".format(url), json={"user_id": bot_id}).json()
    rooms = []
    for room in request:
        rooms.append(room["id"])

    # The more rooms the lesser chance of creating a new one
    if random.random() <= 1 / (len(rooms) + 1):
        # Creates a new room with a random name
        return "/create " + uuid.uuid4().hex[:4]
    else:
        # Joins a room from the list of rooms
        room = "/join " + random.choice(rooms)
        in_room = True
        return room


# Will decide if bot leaves or exits
def leave(chance):
    # Number is smaller than chance, if it is the it leaves
    if random.random() <= chance:
        return True
    else:
        return False


# Goes through different phases: login, join/create room, and then finally send message.
# Then depending on the bot name it sends different messages
def bot_message():
    global in_room
    global bot_name
    global leave_chance
    global exit_chance
    global messages_sent
    global total_messages_sent

    if leave(exit_chance):
        return "/exit"
    else:
        exit_chance = (1 + total_messages_sent) / (50 + total_messages_sent)

    if not in_room:
        return join()

    elif leave(leave_chance):
        # Resets variables connected to being in a room
        messages_sent = 0
        leave_chance = -1
        in_room = False
        return "/leave"
    else:
        leave_chance = (1 + messages_sent) / (8 + messages_sent)

    # Different bots with different messages.
    if bot_name == "Bot_Tobias":
        messages = [
            "樂高生化戰士 是樂高積木由",
            "故事載體在2003年時變為小說和漫畫兩種",
            "並由樂高的新系列《英雄工廠》",
            "년에 처음으로 만들어졌으며",
            "吃那个成寒鸡. 地牢里的金正"
        ]

        messages_sent += 1
        total_messages_sent += 1
        return random.choice(messages)

    elif bot_name == "Bot_William":
        messages = [
            "I used to ride a unicycle as a kid",
            "My favorite song is Bohemian rhapsody by Queen",
            "My hair is long and lushy, like olive oil",
            "As a kid my favorite show was Caillou",
            "Man, I love me some homemade pizza"
        ]

        messages_sent += 1
        total_messages_sent += 1
        return random.choice(messages)

    elif bot_name == "Bot_Eirik":
        messages = [
            "Now I need to ponder my existence and ask myself if I'm truly real.",
            "From time to time I do wonder what is the meaning of my existence.",
            "Every other wednesday I take a trip in the forrest to check if my time has come.",
            "Working in retail makes you appreciate the little things in life",
            "Tomorrow will bring something new, so leave today as a memory.",
            "Choosing to do nothing is still a choice, after all."
        ]

        messages_sent += 1
        total_messages_sent += 1
        return random.choice(messages)

    elif bot_name == "Bot_Adrian":
        messages = [
            "Chocolate covered crickets is my favorite snack.",
            "Did you know it's not possible to convince a monkey to give you a banana by promising it infinite "
            "bananas when they die.",
            "I don’t respect anybody who can’t tell the difference between Pepsi and Coke.",
            "Did you know I was on the Hindenburg when it crashed.",
            "Various sea birds are elegant, but nothing is as elegant as a gliding pelican."
        ]

        messages_sent += 1
        total_messages_sent += 1
        return random.choice(messages)

