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
import cancelledLogs

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

def convertETHtoUSD(amount_in_eth):
    amount_in_USD = amount_in_eth * 1170.69
    return amount_in_USD
    
@app.route("/modifyWallet",methods=['POST'])
def addToWallet():
    data = request.get_json(force=True)
    trader_id = int(data['initiator_id'])
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
def buyNFT():
    if request.method == 'GET':
        #data = request.get_json(force=True)
        data = request.args
        trader_id = int(data['trader_id'])
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.getBuyDetails(trader_id,contract_addr,token_id)
        return Response(out,mimetype='application/json')
    elif request.method == "POST":
        data = request.get_json(force=True)
        trader_id = int(data['trader_id'])
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        commission_type = data['commission_type']
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.buyNFT(trader_id,contract_addr,token_id,commission_type)
        return Response(out,mimetype='application/json')

@app.route("/getTransactionHistory",methods =['GET'])
def getTransactions():
    args = request.args
    trader_id = args['trader_id']
    walletTransaction = WalletTransaction.WalletTransaction()
    walletOut = walletTransaction.getWalletTransactions(trader_id)
    nftTransactionOut = NFTTransaction.NFTTransaction()
    nftOut = nftTransactionOut.getNFTTransactionDetails(trader_id)
    # make a union of jsons and return
    i = 0
    out = {}
    if walletOut != None:
        for each in walletOut:
            out[i] = walletOut[each]
            i=i+1
    if nftTransactionOut != None:
        for eac in nftOut:
            out[i] = nftOut[eac]
            i=i+1
    
    print(json.dumps(out),file=sys.stderr)
    return Response(json.dumps(out),mimetype='application/json')


# code for cancelled logs
# assumption is to get a transid ,time stamp, logInfo from client
@app.route("/cancelNFTTransaction",methods=['POST'])
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
    return Response(json.dumps(transout),mimetype='application/json')

@app.route("/sellNFT",methods =['GET','POST'])
def getsellDetails():
    if request.method == 'GET':
        #data = request.get_json(force=True)
        data = request.args
        trader_id = int(data['trader_id'])
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.getSellDetails(trader_id,contract_addr,token_id)
        return Response(out,mimetype='application/json')
    elif request.method == 'POST':
        data = request.get_json(force=True)
        trader_id = int(data['trader_id'])
        contract_addr = data['contract_addr']
        token_id = data['token_id']
        commission_type = data['commission_type']
        receiver_eth_addr = data['receiver_eth_addr']
        nftTrans = NFTTransaction.NFTTransaction()
        out = nftTrans.sellNFT(trader_id,contract_addr,token_id,receiver_eth_addr,commission_type)
        return Response(out,mimetype='application/json')


if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("4000")
    )
