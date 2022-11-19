from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import Login
import sys
import json
import SignUp
import Home
from flask import Response

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
        return Response(json.dumps(res),mimetype='application/json')
    uid = out[0]
    ty = out[1]
    if ty == 0:
        json_out = oLogin.get_trader_data(uid)
    return Response(json_out,mimetype='application/json')


#### Sign Up

@app.route("/signUp",methods=['POST'])
def signUp():
    data = request.get_json(force=True)
    oSignUp = SignUp.SignUp(data['first_name'],data['last_name'],data['eth_address'],"silver",data['email'],data['cell_no'],data['ph_no'],data['street_addr'],data['city'],data['state'],data['zip'],data['username'],data['password'],0)
    oSignUp.createTrader()
    return Response(status=200)

@app.route("/getNFTDataForHome",methods=['GET'])
def getNFTDataforHome():
    #data = request.get_json(force=True)
    args = request.args
    #t_id = data['t_id']
    trader_id = args['trader_id']
    oHome = Home.Home();
    out = oHome.getnftDataForHome(trader_id)
    return Response(out,mimetype='application/json')


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("4000")
    )
