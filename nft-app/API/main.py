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
import NFTTransaction
import Transaction
import manager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required,get_jwt_identity
import sys
import requests


# initialize flask API
app = Flask(__name__)
api = CORS(app)
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY']= 'ueir09uf9DSHKJDHW92bkFEF0329RFEWRzd'
jwt = JWTManager(app)

@jwt.expired_token_loader
def app_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(res="failed", message="Token has Expired, Please logout and login again"), 401

@jwt.unauthorized_loader
@jwt.invalid_token_loader
def app_unauthorized_callback(jwt_payload):
    return jsonify(res="failed", message="UnAuthorized, Please logout and login again"), 401

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
    else:
        json_out = oLogin.get_manager_data(uid)
    return Response(json_out,mimetype='application/json')


#### Sign Up

@app.route("/signUp",methods=['POST'])
def signUp():
    data = request.get_json(force=True)
    oSignUp = SignUp.SignUp(data['first_name'],data['last_name'],data['eth_address'],"silver",data['email'],data['cell_no'],data['ph_no'],data['street_addr'],data['city'],data['state'],data['zip'],data['username'],data['password'],0)
    out  = oSignUp.createTrader()
    return Response(out,mimetype='application/json')

@app.route("/getNFTDataForHome",methods=['GET'])
@jwt_required()
def getNFTDataforHome():
    #data = request.get_json(force=True)
    args = request.args
    #t_id = data['t_id']
    trader_id = int(args['trader_id'])
    uid = int(get_jwt_identity())
    if trader_id != uid:
        res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
        return Response(json.dumps(res),mimetype='application/json',status=401)
    print(uid,file=sys.stderr)
    oHome = Home.Home()
    out = oHome.getnftDataForHome(trader_id)
    return Response(out,mimetype='application/json')

@app.route("/getNFTDataForTrader",methods=['GET'])
@jwt_required()
def getNFTDataforTrader():
    #data = request.get_json(force=True)
    args = request.args
    #t_id = data['t_id']
    trader_id = int(args['trader_id'])
    uid = int(get_jwt_identity())
    if trader_id != uid:
        res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
        return Response(json.dumps(res),mimetype='application/json',status=401)
    oHome = Home.Home()
    out = oHome.getnftDataForTrader(trader_id)
    return Response(out,mimetype='application/json')

@app.route("/convertETH",methods=['GET'])
def convertUSDtoEth():
    args = request.args
    amount_in_eth =  float(args['amount_in_eth'])
    response = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
    json_data = response.json()
    eth_in_USD = float(json_data['data']['amount'])
    amount_in_USD = amount_in_eth * eth_in_USD
    res = {"amountUSD" : amount_in_USD}
    return Response(json.dumps(res),mimetype='application/json')

def convertETHtoUSD(amount_in_eth):
    response = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
    json_data = response.json()
    eth_in_USD = float(json_data['data']['amount'])
    amount_in_USD = amount_in_eth * eth_in_USD
    return amount_in_USD
    
@app.route("/modifyWallet",methods=['POST'])
@jwt_required()
def addToWallet():
    data = request.get_json(force=True)
    trader_id = int(data['initiator_id'])
    uid = int(get_jwt_identity())
    if trader_id != uid:
        res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
        return Response(json.dumps(res),mimetype='application/json',status=401)
    wallet_trans_type = data['wallet_trans_type']
    amount_in_eth = float(data['amount_in_eth'])
    amount_in_usd = float(convertETHtoUSD(amount_in_eth))
    payment_addr = data['payment_addr']
    wt = WalletTransaction.WalletTransaction(trader_id,"wallet",wallet_trans_type,amount_in_eth,amount_in_usd,payment_addr)
    if wallet_trans_type == "add":
        out = wt.addToWallet()
    elif wallet_trans_type == "withdraw":
        out = wt.removeFromWallet()
    else:
        out = {"res":"failed","message":"Unknown option for wallet_trans_type"}
    return Response(out,mimetype='application/json')

@app.route("/buyNFT",methods=['GET','POST'])
@jwt_required()
def buyNFT():
    if request.method == 'GET':
        #data = request.get_json(force=True)
        data = request.args
        trader_id = int(data['trader_id'])
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        uid = int(get_jwt_identity())
        if trader_id != uid:
            res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
            return Response(json.dumps(res),mimetype='application/json',status=401)
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.getBuyDetails(trader_id,contract_addr,token_id)
        return Response(out,mimetype='application/json')
    elif request.method == "POST":
        data = request.get_json(force=True)
        trader_id = int(data['trader_id'])
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        commission_type = data['commission_type']
        uid = int(get_jwt_identity())
        if trader_id != uid:
            res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
            return Response(json.dumps(res),mimetype='application/json',status=401)
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.buyNFT(trader_id,contract_addr,token_id,commission_type)
        return Response(out,mimetype='application/json')

@app.route("/getTransactionHistory",methods =['GET'])
@jwt_required()
def getTransactions():
    args = request.args
    trader_id = int(args['trader_id'])
    uid = int(get_jwt_identity())
    if trader_id != uid:
        res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
        return Response(json.dumps(res),mimetype='application/json',status=401)
    walletTransaction = WalletTransaction.WalletTransaction()
    walletOut = walletTransaction.getWalletTransactions(trader_id)
    nftTransactionOut = NFTTransaction.NFTTransaction()
    nftOut = nftTransactionOut.getNFTTransactionDetails(trader_id)
    # make a union of jsons and return
    print(walletOut,file=sys.stderr)
    print(nftOut ,file=sys.stderr)
    i = 0
    out = {}
    if walletOut != None:
        print("loop1" ,file=sys.stderr)
        for each in walletOut:
            out[i] = walletOut[each]
            i=i+1
    if nftOut != None:
        print("loop2" ,file=sys.stderr)
        for eac in nftOut:
            out[i] = nftOut[eac]
            i=i+1
    
    print(json.dumps(out),file=sys.stderr)
    return Response(json.dumps(out),mimetype='application/json')


# code for cancelled logs
# assumption is to get a transid ,time stamp, logInfo from client
@app.route("/cancelNFTTransaction",methods=['POST'])
@jwt_required()
def cancelNFTTransactions():
    data = request.get_json(force=True)
    transactionId = data['trans_id']
    logInfo = data['log_info']
    timeStamp = data['time_stamp']
    #nfttransaction 
    print("trans:"+ str(transactionId), file=sys.stderr)
    print("LOGINFO:"+logInfo, file=sys.stderr)
    print("timestamp:"+str(timeStamp), file=sys.stderr)
    trans = Transaction.Transaction()
    transout = trans.cancelTransaction(transactionId,timeStamp,logInfo)
    print(transout, file= sys.stderr)
    out = json.loads(transout)
    return Response(json.dumps(out),mimetype='application/json')

@app.route("/sellNFT",methods =['GET','POST'])
@jwt_required()
def getsellDetails():
    if request.method == 'GET':
        #data = request.get_json(force=True)
        data = request.args
        trader_id = int(data['trader_id'])
        uid = int(get_jwt_identity())
        if trader_id != uid:
            res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
            return Response(json.dumps(res),mimetype='application/json',status=401)
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.getSellDetails(trader_id,contract_addr,token_id)
        return Response(out,mimetype='application/json')
    elif request.method == 'POST':
        data = request.get_json(force=True)
        trader_id = int(data['trader_id'])
        uid = int(get_jwt_identity())
        if trader_id != uid:
            res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
            return Response(json.dumps(res),mimetype='application/json',status=401)
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        commission_type = data['commission_type']
        receiver_eth_addr = data['receiver_eth_addr']
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.sellNFT(trader_id,contract_addr,token_id,receiver_eth_addr,commission_type)
        return Response(out,mimetype='application/json')

@app.route("/createManager",methods=['POST'])
@jwt_required()
def createManager():
        #attr tbd
        data = request.get_json(force=True)
        managerUsername = data['manager_username']
        managerPassword = data['manager_password']
        managerFirstName = data['manager_fname']
        managerLastName = data['manager_lname']
        managerLevel = data['manager_level']
        initiator_id = int(data['initiator_id'])
        uid = int(get_jwt_identity())
        if initiator_id != uid:
            res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
            return Response(json.dumps(res),mimetype='application/json',status=401)
        print(managerUsername,file=sys.stderr)
        print(managerPassword,file=sys.stderr)
        print(managerFirstName,file=sys.stderr)
        print(managerLevel,file=sys.stderr)
        managerInstance = manager.manager(managerUsername,managerPassword,managerFirstName,managerLastName,managerLevel)
        print(managerLastName,file=sys.stderr)
        out = managerInstance.createManager()
        return Response(json.dumps(out),mimetype='application/json')

@app.route("/getReports",methods=['GET'])
@jwt_required()
def getReports():
    #aggregrate info here
    data = request.args
    fromDate = data['from_date']
    toDate = data['to_date']
    fromDate = fromDate +" "+"00:00:00"
    toDate = toDate +" "+"23:59:00"
    print(fromDate,file=sys.stderr)
    print(toDate,file=sys.stderr)
    initiator_id = int(data['initiator_id'])
    uid = int(get_jwt_identity())
    if initiator_id != uid:
        res = {"res":"failed","message":"UnAuthorized, Please logout and login again"}
        return Response(json.dumps(res),mimetype='application/json',status=401)
    #aggregates from transaction
    # transaction table : total no of wallet , nft , total transactions
    transInfo = Transaction.Transaction()
    out1 = transInfo.getTransAggregateInfo(fromDate,toDate)
    #print(out1,file=sys.stderr)
    # wallet : add, withdraws , added amount  , with drawn amount
    walletInfo = WalletTransaction.WalletTransaction()
    out2 = walletInfo.getWalletTransAggregateInfo(fromDate,toDate)
    #print(out2,file=sys.stderr)
    # nft : no of buys , no of sells ,volume of buy in eth , usd , volume of sell in eth , usd , no of cancelled transactions
    nftInfo = NFTTransaction.NFTTransaction()
    out3 = nftInfo.getNFTTransAggregateInfo(fromDate,toDate)
    #print(out3['res'],file=sys.stderr)
    print(out1)
    print(out2)
    print(out3)
    i = 0
    out = {}
    if out1 != None:
        for itr in out1:
            out.update({itr:out1[itr]})
            i = i+1
    if out2 != None:
        for itr2 in out2:
            out.update({itr2:out2[itr2]})
            i = i+1
    if out3 != None:
        for itr3 in out3:
            out.update({itr3:out3[itr3]})
            i = i+1
    print(out,file=sys.stderr)
    return Response(json.dumps(out),mimetype='application/json')


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("4000")
    )
