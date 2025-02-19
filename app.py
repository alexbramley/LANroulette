from flask import Flask, render_template, url_for, request, redirect
from flask_socketio import SocketIO, emit
import socket

app = Flask(__name__)
socketio = SocketIO(app)

PORT_NUMBER = 42069

users = {} # this dict contains {ip: user}

class User:
    def __init__(self, ip_address, nickname, pfp_index):
        self.ip_address = ip_address
        self.nickname = nickname
        self.pfp_index = pfp_index

chatlog = []

user_data = []


@app.route('/', methods=['POST','GET'])
def index():
    ip = request.remote_addr

    if request.method == 'GET':
        if users.__contains__(ip):
            return redirect('/GAMING')
        else:
            message = "hello new person"
            

        return render_template('index.html', ip=ip, message=message)
    
    else:
        nickname = request.form['getnickname']
        if nickname == "":
            return redirect('/')
        users.update({ip: User(ip, nickname, 0)})
        user_data.append([str(ip), str(nickname)])
        chatlog.append(f"{nickname} is here.")
        socketio.emit("update_chatlog", chatlog, include_self=True)
        socketio.emit("update_players", user_data, include_self=True)
        return redirect('/GAMING')



@app.route('/GAMING', methods=['POST','GET'])
def gaming():
    ip = request.remote_addr

    if not users.__contains__(ip):
        return redirect('/')
    
    return render_template('gaming.html', chatlog=chatlog, players=users, player_data=user_data)


@socketio.on("send_message")
def handle_message(data):
    message = data["message"]
    chatlog.append(message)
    emit("update_chatlog", chatlog, broadcast=True)

hostname = socket.gethostname()
hostipaddress = socket.gethostbyname(hostname)

if __name__ == "__main__":
    app.run(host=hostipaddress, port=PORT_NUMBER, debug=True)