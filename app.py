from flask import Flask, render_template, url_for, request
import socket

PORT_NUMBER = 42069

app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    ip = request.remote_addr
    return render_template('index.html', ip=ip)

hostname=socket.gethostname()
hostipaddress = socket.gethostbyname(hostname)

if __name__ == "__main__":
    app.run(host=hostipaddress, port=PORT_NUMBER, debug=True)