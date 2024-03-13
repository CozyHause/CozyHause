from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, emit, SocketIO
import random
from string import ascii_uppercase
import time

app = Flask(__name__)
app.config["SECRET_KEY"] = "verrriii_Sekretttt_kIeyeee__:DDDD"
socketio = SocketIO(app)

hauses = {}

placeholder = [
    "Enter your beautiful name!",
    "Enter your creative name!",
    "Enter your unique name!",
    "Enter your charming name!",
    "Enter your amazing name!",
    "Enter your bombastic name!",
    "Enter your exquisite name!",
    "Enter your distinguished name!",
    "Enter your catchy name!",
    "Enter your elegant name!",
]

enterVerb = [
    "entered",
    "joined",
    "jumped into",
    "barged into",
    "set foot in"
]

leaveVerb = [
    "barged out of",
    "set foot out of",
    "jumped out of",
    "left"
]

nword_list = [
    "nigga",
    "niiga",
    "niggaa",
    "niggaaa",
    "niggaaaa",
    "niigga",
    "nigger",
    "niga",
    "niger",
    "nigggggerr",
    "niggerrr",
    "niggerrrr",
]

def convert_nth(n):
    nstr = str(n)
    if nstr[-1] == "1":
        return nstr + "st"
    elif nstr[-1] == "2":
        return nstr + "nd"
    elif nstr[-1] == "3":
        return nstr + "rd"
    else:
        return nstr + "th"

def onlyornot(members):
    if members <= 3:
        return " only "
    else:
        return " "

def memberOrMembers(members):
    if members == 1:
        return "member"
    else:
        return "members"

def generateCode(length):
    while True:
        code = ""
        for i in range(length):
            code += random.choice(ascii_uppercase)

        if code not in hauses:
            break

    return code

@app.route('/', methods=["GET", "POST"])
def home():
    session.clear()
    if request.method == "POST":
        #retrieve info from the form#
        name = request.form.get("name")
        code = request.form.get("code")
        hauseName = request.form.get("hauseName")
        favColor = request.form.get("favcolor")
        
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        #---------------------------#

        #check if there is info#
        if not name:
            return render_template("home.html", error="Please enter your Name",
                                  name = name,
                                  code = code,
                                  hauseName = hauseName,
                                  placeholder = random.choice(placeholder))

        if favColor == "Favourite_Color":
            return render_template("home.html", error="Please tell us your Favourite Color!",
                  name = name,
                  code = code,
                  hauseName = hauseName,
                  placeholder = random.choice(placeholder))

        if join != False and not code:
            return render_template("home.html", error="Please enter a Hause Code",
                                  name = name,
                                  code = code,
                                  hauseName = hauseName,
                                  placeholder = random.choice(placeholder))

        if join != False and code not in hauses:
            return render_template("home.html", error="The Hause doesn't exist or you typed the code in lowercase. It's cAsE sEnSiTiVe",
                  name = name,
                  code = code,
                  hauseName = hauseName,
                  placeholder = random.choice(placeholder))

        if create != False and not hauseName:
            return render_template("home.html", error="Please enter your Hause Name",
                                  name = name,
                                  code = code,
                                  hauseName = hauseName,
                                  placeholder = random.choice(placeholder))
        #---------------------#
        
        #on pressing create or join#
        hause = code
        
        if create != False: 
            hause = generateCode(4)
            hauses[hause] = {"messages" : [], "members" : 0, "members_list": [], "name" : hauseName, "owner" : name, "nwords": 0, "code": hause}
        
            session["name"] = name
            session["hause"] = hause
            session["color"] = favColor
    
            return redirect(url_for("hause"))

        else:
            if name in hauses[code]["members_list"]:
                return render_template("home.html", error="A person with the name you chose already exists in the hause! Try a more unique name!",
                      name = name,
                      code = code,
                      hauseName = hauseName,
                      placeholder = random.choice(placeholder))
                
            session["name"] = name
            session["hause"] = hause
            session["color"] = favColor

            return redirect(url_for("hause"))
        #-------------------------#

        #1) in case for create: u create ur own code and store it in the session and create a room
        #2) in case for join: u just store the code entered in the session
        
    return render_template("home.html", placeholder = random.choice(placeholder))

@app.route('/hause', methods=["GET", "POST"])
def hause():
    name = session.get("name")
    hause = session.get("hause")

    if name is None or hause is None or hause not in hauses:
        return redirect(url_for("home"))
        
    return render_template("hause.html", hauseCode=hause, hauseName=hauses[hause]["name"], messageHisory=hauses[hause]["messages"])

@app.route('/discover', methods=["POST", "GET"])
def discover():
    session.clear()
    if request.method == "POST":
        #retrieve info from the form#
        name = request.form.get("name")
        favColor = request.form.get("favcolor")
        code = request.form.get("hauseCode")
        
        #check for info
        if not name:
            return render_template("discover.html", error="Please enter your Name",
                                  name = name,
                                  placeholder = random.choice(placeholder),
                                  public_hauses = hauses)

        if favColor == "Favourite_Color":
            return render_template("discover.html", error="Please tell us your Favourite Color!",
                  name = name,
                  placeholder = random.choice(placeholder), public_hauses = hauses)

        if code in hauses and name in hauses[code]["members_list"]:
            return render_template("discover.html", error="A person with the name you chose already exists in the hause! Try a more unique name!",
                  name = name,
                  placeholder = random.choice(placeholder),
                  public_hauses = hauses)

        #do stuff
        session["name"] = name
        session["hause"] = code
        session["color"] = favColor

        return redirect(url_for("hause"))

    return render_template("discover.html", public_hauses=hauses, placeholder=random.choice(placeholder))

@app.route('/home', methods=['GET', 'POST'])
def home_redirect():
    return redirect(url_for("home"))

@socketio.on("connect")
def connect():
    name = session.get("name")
    hause = session.get("hause")
    hauseName = hauses[hause]["name"]

    join_room(hause)

    hauses[hause]["members"] += 1
    hauses[hause]["members_list"].append(name)

    ordinal = convert_nth(hauses[hause]["members"])
    randomEnterVerb = random.choice(enterVerb)

    #emit a msg
    join_message = f"{name} has {randomEnterVerb} the Hause"
    join_messageMemberCount = f"{name} is the " #ordinal member of hauseName

    emit("join_leave", {"message" : join_message, "date": time.ctime()}, room=hause)
    emit("memberCount_join", {"message" : join_messageMemberCount, "members" : ordinal, "hauseName" : hauseName}, room=hause)

    #for debugging
    print(f"{name} has {random.choice(enterVerb)} the Hause and is the {ordinal} member of '{hauseName}'. Code: {hause}")

@socketio.on("disconnect")
def disconnect():
    name = session.get("name")
    hause = session.get("hause")
    hauseName = hauses[hause]["name"]

    leave_room(hause)
    
    hauses[hause]["members"] -= 1
    hauses[hause]["members_list"].remove(name)
    if hauses[hause]["members"] <= 0:
        del hauses[hause]

    if hauses[hause]["members"] > 0:
        only = onlyornot(hauses[hause]["members"])
        randomLeaveVerb = random.choice(leaveVerb)
        memberOrMembers_text = memberOrMembers(hauses[hause]["members"])
        
        #emit a msg
        leave_message = f"{name} has {randomLeaveVerb} the Hause"
        leave_messageMemberCount = f"'{hauseName}' now{only}has " #{members} members
        
        emit("join_leave", {"message" : leave_message, "date": time.ctime()}, room=hause)
        emit("memberCount_leave", {"message" : leave_messageMemberCount, "members" : hauses[hause]["members"], "membersText" : memberOrMembers_text}, room=hause)

        #for debugging
        print(f"{name} has left the Hause. '{hauseName}' now{only}has {hauses[hause]['members']} members. Code: {hause}")

@socketio.on("chatMessage")
def chatMessage(message):
    name = session.get("name")
    hause = session.get("hause")
    color = session.get("color")

    message_to_be_sent = {
        "name" : name,
        "message" : message["message"],
        "date" : time.ctime(),
        "color" : color
    }

    emit("chatMessage_send", message_to_be_sent, room=hause)

    #N-Word Counter
    for i in nword_list:
        if i in message["message"].lower():
            hauses[hause]["nwords"] += 1
            emit("nwordcounter", {"nwords" : hauses[hause]["nwords"]}, room=hause)
            break

    #for debugging
    print(f"{name} said {message['message']}. Code: {hause}")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=False, allow_unsafe_werkzeug=True)
