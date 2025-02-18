from flask import Flask, render_template, url_for, request, redirect
import socket

PORT_NUMBER = 42069

users = {} # this dict contains {ip: user}

class User:
    def __init__(self, ip_address, nickname):
        self.ip_address = ip_address
        self.nickname = nickname

chatlog = []

app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def index():
    ip = request.remote_addr

    if request.method == 'GET':
        if users.__contains__(ip):
            message = "welcome back"
        else:
            message = "hello new person"
            users.update({ip: User(ip, "<PLACEHOLDER>")})

        return render_template('index.html', ip=ip, message=message)
    
    else:
        nickname = request.form['getnickname']
        users[ip].nickname = nickname
        chatlog.append(f"{nickname} is here.")
        return redirect('/GAMING')

@app.route('/GAMING', methods=['POST','GET'])
def gaming():
    return render_template('gaming.html', chatlog=chatlog)

hostname=socket.gethostname()
hostipaddress = socket.gethostbyname(hostname)

if __name__ == "__main__":
    app.run(host=hostipaddress, port=PORT_NUMBER, debug=True)