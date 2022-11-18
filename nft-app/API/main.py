from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import Login
import sys
import json

# initialize flask API
app = Flask(__name__)
api = CORS(app)


@app.route("/")
def home():
    return "<h1>NFT APP</h1>"

#### LOGIN API  ####

@app.route("/login", methods=['POST', 'GET'])
def login():
    data = request.get_json(force=True)
    username = data['username']
    password = data['password']
    oLogin = Login.Login(username, password)
    print(password, file=sys.stderr)
    out = oLogin.check_type()
    #getc_details = oLogin.get_client_data()
    if out[2] == "failed":
        res  = {"res":"failed"}
        return json.dumps(res)
    uid = out[0]
    ty = out[1]
    if ty == 0:
        json_out = oLogin.get_trader_data(uid)
    return json_out

if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("4000")
    )
