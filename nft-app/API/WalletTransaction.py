import pandas as pd
from pandas.io import json
import config as cg
import sys
from datetime import datetime as dt

class WalletTransaction:

    def __init__(self) -> None:
        pass

    def __init__(self,initiator_id=None,trans_type=None,wallet_trans_type=None,amount_in_eth=None,amount_in_usd=None,payment_addr=None):
        self.initiator_id=initiator_id
        self.trans_type=trans_type
        self.wallet_trans_type=wallet_trans_type
        self.amount_in_eth=amount_in_eth
        self.amount_in_usd=amount_in_usd
        self.payment_addr=payment_addr

    def addToWallet(self):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            qry = f"INSERT INTO test.transaction(trans_type) VALUES('{self.trans_type}')"
            cursor.execute(qry)
            qry_trans_id = f"SELECT * FROM test.transaction ORDER BY trans_id DESC LIMIT 1"
            df = pd.read_sql(qry_trans_id,conn)
            trans_id = int(df['trans_id'][0])

            qry1 = f"INSERT INTO test.wallet_transaction(trans_id,initiator_id,wallet_trans_type,amount_in_usd,amount_in_eth,payment_addr) values({trans_id},{self.initiator_id},'{self.wallet_trans_type}',{self.amount_in_usd},{self.amount_in_eth},'{self.payment_addr}')"
            cursor.execute(qry1)
            print("before select wallet balance", file=sys.stderr)
            qry2 = f"SELECT wallet_balance FROM test.trader WHERE t_id={self.initiator_id}"
            df = pd.read_sql(qry2,conn)
            print(df, file=sys.stderr)
            curr_balance = float(df['wallet_balance'][0])
            print(curr_balance, file=sys.stderr)
            updated_balance = curr_balance + self.amount_in_eth
            print(updated_balance, file=sys.stderr)
            qry3 = f"UPDATE test.trader SET wallet_balance={updated_balance} where t_id={self.initiator_id}"
            cursor.execute(qry3)
            cursor.close()
            res = {"res":"success","message":"transaction successful","updated_balance":updated_balance}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def removeFromWallet(self):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            qry2 = f"SELECT wallet_balance FROM test.trader WHERE t_id={self.initiator_id}"
            df = pd.read_sql(qry2,conn)
            print(df, file=sys.stderr)
            curr_balance = float(df['wallet_balance'][0])
            if curr_balance < self.amount_in_eth:
                res = {"res":"failed","message":"Cannot withdraw the amount (you don't have enough balance in your account)"}
                return json.dumps(res)
            qry = f"INSERT INTO test.transaction(trans_type) VALUES('{self.trans_type}')"
            cursor.execute(qry)
            qry_trans_id = f"SELECT * FROM test.transaction ORDER BY trans_id DESC LIMIT 1"
            df = pd.read_sql(qry_trans_id,conn)
            trans_id = int(df['trans_id'][0])

            qry1 = f"INSERT INTO test.wallet_transaction(trans_id,initiator_id,wallet_trans_type,amount_in_usd,amount_in_eth,payment_addr) values({trans_id},{self.initiator_id},'{self.wallet_trans_type}',{self.amount_in_usd},{self.amount_in_eth},'{self.payment_addr}')"
            cursor.execute(qry1)
            updated_balance = curr_balance - self.amount_in_eth
            print(updated_balance, file=sys.stderr)
            qry3 = f"UPDATE test.trader SET wallet_balance={updated_balance} where t_id={self.initiator_id}"
            cursor.execute(qry3)
            cursor.close()
            res = {"res":"success","message":"transaction successful","updated_balance":updated_balance}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)
    
    def getWalletTransactions(self,trader_id):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            # write our query here
            sqlQuery = f"SELECT T.trans_id,trans_time,trans_type,initiator_id,wallet_trans_type,amount_in_eth,amount_in_usd,payment_addr FROM transaction T , wallet_transaction W where T.trans_id = W.trans_id AND W.initiator_id = {trader_id} "
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