import pandas as pd
from pandas.io import json
import config as cg
import sys
import cancelledLogs
from datetime import datetime as dt,tzinfo, timezone
from pandas import Timestamp

import requests

class NFTTransaction:
    def __init__(self,initator_id=None,receiver_id=None,contract_address=None,token_id=None,total_amount=None,commission=None,commission_type=None,nft_trans_type=None,trans_status=None):
        self.initiator_id = initator_id
        self.receiver_id= receiver_id
        self.contract_address = contract_address
        self.token_id = token_id
        self.total_amount = total_amount
        self.commission = commission
        self.commission_type = commission_type
        self.nft_trans_type = nft_trans_type
        self.trans_status = trans_status


    def getNFTTransAggregateInfo(self,fromDate,toDate):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            sql1 = f"SELECT COUNT(*) AS cancelledTrans  FROM nft_transaction W, transaction T WHERE W.trans_id = T.trans_id AND  T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.trans_status = '{'cancelled'}'"
            df1 = pd.read_sql(sql1,conn)
            #print(df1,file = sys.stderr)
            cancelledTrans = int(df1['cancelledTrans'][0])
            sql2 = f"SELECT COUNT(*) AS successTrans  FROM nft_transaction W, transaction T WHERE W.trans_id = T.trans_id AND  T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.trans_status = '{'successful'}'"
            df2 = pd.read_sql(sql2,conn)
            #print(df2,file = sys.stderr)
            successTrans = int(df2['successTrans'][0])
            sql3 = f"SELECT SUM(W.total_amount) AS total  FROM nft_transaction W, transaction T WHERE W.trans_id = T.trans_id AND  T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.trans_status = '{'successful'}'"
            df3 = pd.read_sql(sql3,conn)
            #print(df3,file = sys.stderr)
            if df3['total'][0] != None:
                total = float(df3['total'][0])
            else:
                total = 0.0
            res = {"cancelledTransactions":cancelledTrans,"successfulTransactions":successTrans,"totalAmountInEth":total}
            #res = {}
            #res.update({"cancelledTransactions":cancelledTrans})
            #res.update({"successfulTransactions":successTrans})
            #res.update({"totalAmountInEth":total})
            return res
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def cancelNFTTransaction(self,transactionID,timestamp,logInfo):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            # check if the status is cancelled
            sql1 = f"SELECT trans_status FROM nft_transaction WHERE trans_id = {transactionID}"
            df1 = pd.read_sql(sql1,conn)
            transStatusFromTable = df1['trans_status'][0]
            if transStatusFromTable != "cancelled":
                sql = f"UPDATE nft_transaction SET trans_status = 'cancelled'  WHERE trans_id = {transactionID}"
                cursor.execute(sql)
                #print("NFTtransaction update executed " ,file=sys.stderr)
                #cancelledlog
                cl= cancelledLogs.cancelledLogs(trans_id=transactionID,log_info=logInfo,log_trans_time=timestamp)
                clout = cl.addLogs()
                res = {"res":"successful","message":"Transaction Successful","trans_id":{transactionID}}
                return res
            else:
                res = {"res":"failed","message":"Transaction has already been cancelled"}
                return res
            
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return res


    def getNFTTransactionDetails(self,trader_id):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            sqlQuery = f"SELECT T.trans_id,T.trans_time,T.trans_type,W.initiator_id,W.receiver_id,W.contract_addr,W.token_id,W.total_amount,W.commission_in_eth,W.commission_in_usd,W.commission_type,W.nft_trans_type,W.trans_status FROM transaction T , nft_transaction W where T.trans_id = W.trans_id AND W.initiator_id = {trader_id} "
            df = pd.read_sql(sqlQuery,conn)
            #print(df, file=sys.stderr)
            if not df.empty:
                json_nft_data = df.to_json(orient = "index")
                parsed_json = json.loads(json_nft_data)
                #print(type(json_nft_data))
                #print(df,file=sys.stderr)
                for iter in parsed_json:
                    #print(type(iter),file =sys.stderr)
                    transTime = df['trans_time'][int(iter)]
                    transTimeDT = Timestamp.to_pydatetime(transTime)
                    #print(transTime,file = sys.stderr)
                    #print(transTimeDT,file = sys.stderr)
                    #print(transTime,file=sys.stderr)
                    parsed_json[iter].update({"trans_dateTime":str(transTimeDT)})
                return parsed_json
            else:
                return None
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)
    
    def getBuyDetails(self,trader_id,contract_addr,token_id):
        try:
            conn = cg.connect_to_mySQL()
            #cursor = conn.connect()
            qry = f"SELECT t_id,trader_level,wallet_balance FROM trader where t_id={trader_id}"
            df1 = pd.read_sql(qry,conn)
            wallet_balance = float(df1['wallet_balance'][0])
            trader_level = df1['trader_level'][0]

            qry1 = f"SELECT * FROM nft where contract_addr = '{contract_addr}' and token_id = '{token_id}'"
            df2 = pd.read_sql(qry1,conn)
            nft_price = df2["current_price"][0]
            if nft_price > wallet_balance:
                res = {"res":"failed","message":"Unable to proceed with transaction: Insufficent Wallet balance"}
                return json.dumps(res)
            else:
                df3 = df1.join(df2)
                if trader_level == 'gold':
                    commission_in_eth = (0.5 * nft_price)/100
                elif trader_level == 'silver':
                    commission_in_eth = (nft_price)/100
                else:
                    commission_in_eth = (nft_price)/100
                commission_in_usd = self.convertETHtoUSD(commission_in_eth)
                total_amount = nft_price + commission_in_eth
                json_data = df3.to_json(orient = "index")
                parsed_data = json.loads(json_data)
                parsed_data = parsed_data['0']
                if wallet_balance >= total_amount:
                    parsed_data.update({"options":2})
                else:
                    parsed_data.update({"options":1})
                parsed_data.update({"commission_in_eth":commission_in_eth})
                parsed_data.update({"commission_in_usd":commission_in_usd})
                parsed_data.update({"total_trans_amount":total_amount})
                parsed_data.update({"res":"successful"})
                return json.dumps(parsed_data)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def convertETHtoUSD(self,amount_in_eth):
        response = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
        json_data = response.json()
        eth_in_USD = float(json_data['data']['amount'])
        amount_in_USD = amount_in_eth * eth_in_USD
        return amount_in_USD

    def buyNFT(self,trader_id,contract_addr,token_id,commission_type):
        try:
            conn = cg.connect_to_mySQL()
            cursor = conn.connect()
            qry = f"SELECT trader_level,wallet_balance FROM trader where t_id={trader_id}"
            df1 = pd.read_sql(qry,conn)
            wallet_balance = float(df1['wallet_balance'][0])
            trader_level = df1['trader_level'][0]

            qry1 = f"SELECT * FROM nft where contract_addr = '{contract_addr}' and token_id = '{token_id}'"
            df2 = pd.read_sql(qry1,conn)
            nft_price = df2["current_price"][0]
            current_owner_id = df2["owner_id"][0]
            if nft_price > wallet_balance:
                res = {"res":"failed","message":"Unable to proceed with transaction: Insufficent Wallet balance"}
                return json.dumps(res)
            else:
                #df3 = df1.join(df2)
                if trader_level == 'gold':
                    commission_in_eth = (0.5 * nft_price)/100
                elif trader_level == 'silver':
                    commission_in_eth = (nft_price)/100
                else:
                    commission_in_eth = (nft_price)/100
                commission_in_usd = self.convertETHtoUSD(commission_in_eth)
                total_amount = nft_price + commission_in_eth
                total_amount_in_usd = self.convertETHtoUSD(total_amount)
                if commission_type == 'fiat':
                    updated_balance = wallet_balance - nft_price
                elif commission_type == 'eth':
                    if wallet_balance > total_amount:
                        updated_balance = wallet_balance - total_amount
                    else:
                        res = {"res":"failed","message":"Unable to proceed with transaction: Insufficent Wallet balance to pay commission in ethereum"}
                        return json.dumps(res)
                qry2 = f"INSERT INTO transaction(trans_type) values ('nft')"
                cursor.execute(qry2)
                qry_trans_id = f"SELECT * FROM transaction ORDER BY trans_id DESC LIMIT 1"
                df = pd.read_sql(qry_trans_id,conn)
                trans_id = int(df['trans_id'][0])
                qry3 = f"INSERT INTO nft_transaction(trans_id,initiator_id,receiver_id,contract_addr,token_id,total_amount,total_amount_in_usd,commission_in_eth,commission_in_usd,commission_type,nft_trans_type,trans_status) values ({trans_id},{trader_id},{current_owner_id},'{contract_addr}','{token_id}',{total_amount},{total_amount_in_usd},{commission_in_eth},{commission_in_usd},'{commission_type}','buy','successful')"
                cursor.execute(qry3)
                qry4 = f"UPDATE trader SET wallet_balance={updated_balance} where t_id={trader_id}"
                cursor.execute(qry4)
                qry5 = f"SELECT trader_level,wallet_balance FROM trader where t_id={current_owner_id}"
                df1 = pd.read_sql(qry5,conn)
                receiver_wallet_balance = float(df1['wallet_balance'][0])
                receiver_wallet_balance = receiver_wallet_balance + nft_price
                qry6 = f"UPDATE trader SET wallet_balance={receiver_wallet_balance} where t_id={current_owner_id}"
                cursor.execute(qry6)
                qry7 = f"UPDATE nft SET owner_id={trader_id} where contract_addr = '{contract_addr}' and token_id = '{token_id}'"
                cursor.execute(qry7)
                res = {"res":"successful","message":"Transaction Successful","trans_id":trans_id,"updated_balance":updated_balance}
                return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)
    
    def getSellDetails(self,trader_id,contract_addr,token_id):
        try:
            conn = cg.connect_to_mySQL()
            cursor = conn.connect()
            qry = f"SELECT * FROM nft where contract_addr = '{contract_addr}' and token_id = '{token_id}'"
            df1 = pd.read_sql(qry,conn)
            current_owner = int(df1['owner_id'][0])
            nft_price = float(df1['current_price'][0])
            qry1 = f"SELECT t_id,trader_level,wallet_balance FROM trader where t_id = '{trader_id}'"
            df2 = pd.read_sql(qry1,conn)
            initiator_wallet_balance = int(df2['wallet_balance'][0])
            trader_level = df2['trader_level'][0]
            if trader_level == 'gold':
                commission_in_eth = (0.5 * nft_price)/100
            elif trader_level == 'silver':
                commission_in_eth = (nft_price)/100
            else:
                commission_in_eth = (nft_price)/100
            commission_in_usd = self.convertETHtoUSD(commission_in_eth)
            if current_owner != trader_id:
                res = {"res":"failed","message":"Unable to proceed, NFT is owned by someone else"}
                return json.dumps(res)
            df3 = df1.join(df2)
            json_data = df3.to_json(orient = "index")
            parsed_data = json.loads(json_data)
            parsed_data = parsed_data['0']
            if initiator_wallet_balance < commission_in_eth:
                parsed_data.update({"options":1})
            else:
                parsed_data.update({"options":2})
            parsed_data.update({"commission_in_eth":commission_in_eth})
            parsed_data.update({"commission_in_usd":commission_in_usd})
            parsed_data.update({"res":"successful"})
            return json.dumps(parsed_data)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)
    

    def sellNFT(self,trader_id,contract_addr,token_id,receiver_eth_address,commission_type):
        try:
            conn = cg.connect_to_mySQL()
            cursor = conn.connect()
            qry = f"SELECT * FROM nft where contract_addr = '{contract_addr}' and token_id = '{token_id}'"
            df1 = pd.read_sql(qry,conn)
            current_owner = int(df1['owner_id'][0])
            nft_price = float(df1['current_price'][0])
            qry1 = f"SELECT t_id,trader_level,wallet_balance FROM trader WHERE t_id = '{trader_id}'"
            df2 = pd.read_sql(qry1,conn)
            initiator_wallet_balance = int(df2['wallet_balance'][0])
            trader_level = df2['trader_level'][0]
            if trader_level == 'gold':
                commission_in_eth = (0.5 * nft_price)/100
            elif trader_level == 'silver':
                commission_in_eth = (nft_price)/100
            else:
                commission_in_eth = (nft_price)/100
            commission_in_usd = self.convertETHtoUSD(commission_in_eth)
            total_amount = nft_price + commission_in_eth
            total_amount_in_usd = self.convertETHtoUSD(total_amount)
            if current_owner != trader_id:
                res = {"res":"failed","message":"Unable to proceed, NFT is owned by someone else"}
                return json.dumps(res)
            qry2 = f"SELECT t_id,wallet_balance FROM trader WHERE eth_addr = '{receiver_eth_address}'"
            df3 = pd.read_sql(qry2,conn)
            if not df3.empty:
                receiver_id = df3['t_id'][0]
                receiver_wallet_balance = df3['wallet_balance'][0]
            else:
                res = {"res":"failed","message":"Unable to proceed, Buyer's Ethereum Address not found"}
                return json.dumps(res)
            if receiver_wallet_balance < nft_price:
                res = {"res":"failed","message":"Unable to proceed with transaction: Insufficent Wallet balance on buyer's end"}
                return json.dumps(res)
            if commission_type == 'fiat':
                    receiver_updated_balance = receiver_wallet_balance - nft_price
                    initiator_updated_balance = initiator_wallet_balance + nft_price
            elif commission_type == 'eth':
                receiver_updated_balance = receiver_wallet_balance - nft_price
                initiator_updated_balance = initiator_wallet_balance + nft_price - commission_in_eth
            else:
                res = {"res":"failed","message":"Unable to proceed with transaction: Insufficent Wallet balance to pay commission in ethereum"}
                return json.dumps(res)
            qry3 = f"INSERT INTO transaction(trans_type) values ('nft')"
            cursor.execute(qry3)
            qry_trans_id = f"SELECT * FROM transaction ORDER BY trans_id DESC LIMIT 1"
            df = pd.read_sql(qry_trans_id,conn)
            trans_id = int(df['trans_id'][0])
            qry4 = f"INSERT INTO nft_transaction(trans_id,initiator_id,receiver_id,contract_addr,token_id,total_amount,total_amount_in_usd,commission_in_eth,commission_in_usd,commission_type,nft_trans_type,trans_status) values ({trans_id},{trader_id},{receiver_id},'{contract_addr}','{token_id}',{total_amount},{total_amount_in_usd},{commission_in_eth},{commission_in_usd},'{commission_type}','sell','successful')"
            cursor.execute(qry4)
            qry5 = f"UPDATE trader SET wallet_balance={initiator_updated_balance} where t_id={trader_id}"
            cursor.execute(qry5)
            qry6 = f"UPDATE trader SET wallet_balance={receiver_updated_balance} where t_id={receiver_id}"
            cursor.execute(qry6)
            qry7 = f"UPDATE nft SET owner_id={receiver_id} where contract_addr = '{contract_addr}' and token_id = '{token_id}'"
            cursor.execute(qry7)
            res = {"res":"successful","message":"Transaction Successful","trans_id":trans_id,"updated_balance":initiator_updated_balance}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)