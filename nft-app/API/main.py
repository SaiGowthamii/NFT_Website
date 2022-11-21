from flask import Flask, request, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
import Login
import sys
import json
import SignUp
import Home
import WalletTransaction
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
    out  = oSignUp.createTrader()
    return Response(out,mimetype='application/json')

@app.route("/getNFTDataForHome",methods=['GET'])
def getNFTDataforHome():
    #data = request.get_json(force=True)
    args = request.args
    #t_id = data['t_id']
    trader_id = args['trader_id']
    oHome = Home.Home()
    out = oHome.getnftDataForHome(trader_id)
    return Response(out,mimetype='application/json')

@app.route("/getNFTDataForTrader",methods=['GET'])
def getNFTDataforTrader():
    #data = request.get_json(force=True)
    args = request.args
    #t_id = data['t_id']
    trader_id = args['trader_id']
    oHome = Home.Home()
    out = oHome.getnftDataForTrader(trader_id)
    return Response(out,mimetype='application/json')

@app.route("/convertETH",methods=['GET'])
def convertUSDtoEth():
    args = request.args
    amount_in_eth =  float(args['amount_in_eth'])
    amount_in_USD = amount_in_eth * 1170.69
    res = {"amountUSD" : amount_in_USD}
    return Response(json.dumps(res),mimetype='application/json')

@app.route("/addToWallet",methods=['POST'])
def addToWallet():
    data = request.get_json(force=True)
    trader_id = int(data['initiator_id'])
    amount_in_eth = float(data['amount_in_eth'])
    amount_in_usd = float(data['amount_in_usd'])
    payment_addr = data['payment_addr']
    wt = WalletTransaction.WalletTransaction(trader_id,"wallet",amount_in_eth,amount_in_usd,payment_addr)
    out = wt.addToWallet()
    return Response(out,mimetype='application/json')


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("4000")
    )
