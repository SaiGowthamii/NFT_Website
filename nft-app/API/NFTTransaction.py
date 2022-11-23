import pandas as pd
from pandas.io import json
import config as cg
import sys

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

    def getNFTTransactionDetails(self,trader_id):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            '''trans_id int auto_increment primary key,
        trans_time datetime default current_timestamp,
        trans_type varchar(15)'''
            sqlQuery = f"SELECT T.trans_id,T.trans_time,T.trans_type,W.initiator_id,W.receiver_id,W.contract_addr,W.token_id,W.total_amount,W.commission,W.commission_type,W.nft_trans_type,W.trans_status FROM transaction T , nft_transaction W where T.trans_id = W.trans_id AND W.initiator_id = {trader_id} "
            df = pd.read_sql(sqlQuery,conn)
            print(df, file=sys.stderr)
            if not df.empty:
                json_nft_data = df.to_json(orient = "index")
                parsed_json = json.loads(json_nft_data)
                return json.dumps(parsed_json)
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
                    commission = (0.5 * nft_price)/100
                elif trader_level == 'silver':
                    commission = (nft_price)/100
                else:
                    commission = (nft_price)/100
                total_amount = nft_price + commission
                json_data = df3.to_json(orient = "index")
                parsed_data = json.loads(json_data)
                parsed_data = parsed_data['0']
                if wallet_balance >= total_amount:
                    parsed_data.update({"options":2})
                else:
                    parsed_data.update({"options":1})
                parsed_data.update({"commission":commission})
                parsed_data.update({"total_trans_amount":total_amount})
                return json.dumps(parsed_data)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def buyNFT(self,trader_id,contract_addr,token_id,nft_trans_type):
        try:
            conn = cg.connect_to_mySQL()
            qry = f"SELECT trader_level,wallet_balance FROM trader where t_id={trader_id}"
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
                #df3 = df1.join(df2)
                if trader_level == 'gold':
                    commission = (0.5 * nft_price)/100
                elif trader_level == 'silver':
                    commission = (nft_price)/100
                else:
                    commission = (nft_price)/100
                total_amount = nft_price + commission
                #json_data = df3.to_json(orient = "index")
                #parsed_data = json.loads(json_data)
                #parsed_data = parsed_data['0']
                #if wallet_balance >= total_amount:
                #    parsed_data.update({"options":2})
                #else:
                #    parsed_data.update({"options":1})
                #parsed_data.update({"commission":commission})
                #parsed_data.update({"total_trans_amount":total_amount})
                #return json.dumps(parsed_data)

            return
        except Exception as e:
            return
