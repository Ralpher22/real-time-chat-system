from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketIO import SocketIO, join_room, leave_room, send
import random
from string import ascii_uppercase

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjhjsdahhds'
socketio = SocketIO(app)
rooms = {}


def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            return code


@app.route('/', methods=['POST', 'GET'])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get('name')
        code = request.form.get('code')
        join = request.form.get('join')
        create = request.form.get('create')

        if not name:
            return render_template('home.html', error='Please enter a name')
        
        if join and not code:
            return render_template('home.html', error='Please enter a room code')
        
        if create:
            room = generate_unique_code(4)
            rooms[room] = {'members': 0, 'messages': []}
        elif code not in rooms:
            return render_template('home.html', error='Room does not exist')

        session['room'] = code if join else room
        session['name'] = name
        return redirect(url_for('room'))

    return render_template('home.html')


@app.route('/room')
def room():
    room_code = session.get('room')
    if room_code is None or session.get('name') is None or room_code not in rooms:
        return redirect(url_for('home'))

    return render_template('room.html' code = room,messages=rooms[room]["messages"])
_@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to = room)
    rooms[room]["messages"].append(content)
    print(f"{session.get{'name'} said: {data{'datat'}}}")

@socketio.on("connect")
def connect(auth):
    room =session.grt("room")
    room = session.get("name")
    if not room or not name:
        return
    if nroom not in rooms:
        leave_room(room)
        return
    join_room(room)
    send(("name:" name, "message": "has entered the room"),to=room)
    room[room]["members"] ==1
    print(f"{name} joined room {room}")

    @socketio.on("disconnect")
    def disconnect():
        room = session.get('room')
        name = session.get("name")
        leave_room(room)
    if room in rooms:
        room[room]["members"] = 1
        if room[room]["members"] = 0:
            def rooms[room]
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")
if __name__ == '__main__':
    socketio.run(app, debug=True)