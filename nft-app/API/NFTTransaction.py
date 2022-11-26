import pandas as pd
from pandas.io import json
import config as cg
import sys
import cancelledLogs
from datetime import datetime as dt

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
                print("NFTtransaction update executed " ,file=sys.stderr)
                #cancelledlog
                cl= cancelledLogs.cancelledLogs(trans_id=transactionID,log_info=logInfo,log_trans_time=timestamp)
                clout = cl.addLogs()
                res = {"res":"successful","message":"Transaction Successful","trans_id":{transactionID}}
                return json.dumps(res)
            else:
                res = {"res":"failed","message":"Transaction has already been cancelled"}
                return json.dumps(res)
            
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)


    def getNFTTransactionDetails(self,trader_id):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            sqlQuery = f"SELECT T.trans_id,T.trans_time,T.trans_type,W.initiator_id,W.receiver_id,W.contract_addr,W.token_id,W.total_amount,W.commission_in_eth,W.commission_in_usd,W.commission_type,W.nft_trans_type,W.trans_status FROM transaction T , nft_transaction W where T.trans_id = W.trans_id AND W.initiator_id = {trader_id} "
            df = pd.read_sql(sqlQuery,conn)
            print(df, file=sys.stderr)
            if not df.empty:
                json_nft_data = df.to_json(orient = "index")
                parsed_json = json.loads(json_nft_data)
                for iter in parsed_json:
                    transTime = parsed_json[iter]['trans_time']
                    parsed_json[iter].update({"trans_dateTime":str(dt.fromtimestamp(transTime/1000))})
                return parsed_json
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
                return json.dumps(parsed_data)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def convertETHtoUSD(self,amount_in_eth):
        amount_in_USD = amount_in_eth * 1170.69
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
                qry3 = f"INSERT INTO nft_transaction(trans_id,initiator_id,receiver_id,contract_addr,token_id,total_amount,commission_in_eth,commission_in_usd,commission_type,nft_trans_type,trans_status) values ({trans_id},{trader_id},{current_owner_id},'{contract_addr}','{token_id}',{total_amount},{commission_in_eth},{commission_in_usd},'{commission_type}','buy','successful')"
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
                res = {"res":"successful","message":"Transaction Successful","trans_id":trans_id}
                return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)
