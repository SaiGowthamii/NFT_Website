import pandas as pd
from pandas.io import json
import config as cg
import sys
from datetime import datetime as dt
from pandas import Timestamp

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
            if self.amount_in_eth < 0:
                res = {"res":"failed","message":"amount cannot be negative"}
                return json.dumps(res)
            qry = f"INSERT INTO test.transaction(trans_type) VALUES('{self.trans_type}')"
            cursor.execute(qry)
            qry_trans_id = f"SELECT * FROM test.transaction ORDER BY trans_id DESC LIMIT 1"
            df = pd.read_sql(qry_trans_id,conn)
            trans_id = int(df['trans_id'][0])

            qry1 = f"INSERT INTO test.wallet_transaction(trans_id,initiator_id,wallet_trans_type,amount_in_usd,amount_in_eth,payment_addr) values({trans_id},{self.initiator_id},'{self.wallet_trans_type}',{self.amount_in_usd},{self.amount_in_eth},'{self.payment_addr}')"
            cursor.execute(qry1)
            qry2 = f"SELECT wallet_balance FROM test.trader WHERE t_id={self.initiator_id}"
            df = pd.read_sql(qry2,conn)
            curr_balance = float(df['wallet_balance'][0])
            updated_balance = curr_balance + self.amount_in_eth
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
            if self.amount_in_eth < 0:
                res = {"res":"failed","message":"amount cannot be negative"}
                return json.dumps(res)
            qry2 = f"SELECT wallet_balance FROM test.trader WHERE t_id={self.initiator_id}"
            df = pd.read_sql(qry2,conn)
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
            qry3 = f"UPDATE test.trader SET wallet_balance={updated_balance} where t_id={self.initiator_id}"
            cursor.execute(qry3)
            cursor.close()
            res = {"res":"success","message":"transaction successful","updated_balance":updated_balance}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def getWalletTransAggregateInfo(self,fromDate,toDate):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            sql1 = f"SELECT SUM(W.amount_in_usd) as sumWithdrawWalletUSD,SUM(W.amount_in_eth) as sumWithdrawWalletETH FROM wallet_transaction W, transaction T WHERE W.trans_id = T.trans_id AND  T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.wallet_trans_type='withdraw'"
            df1 = pd.read_sql(sql1,conn)
            if df1['sumWithdrawWalletUSD'][0] != None:
                sumWithdrawWalletUSD = float(df1['sumWithdrawWalletUSD'][0])
            else:
                sumWithdrawWalletUSD = 0.0
            if df1['sumWithdrawWalletETH'][0] != None:
                sumWithdrawWalletETH =  float(df1['sumWithdrawWalletETH'][0])
            else:
                sumWithdrawWalletETH = 0.0
            sql1 = f"SELECT SUM(W.amount_in_usd) as sumAddWalletUSD,SUM(W.amount_in_eth) as sumAddWalletETH FROM wallet_transaction W, transaction T WHERE W.trans_id = T.trans_id AND  T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.wallet_trans_type='add'"
            df1 = pd.read_sql(sql1,conn)
            if df1['sumAddWalletUSD'][0] != None:
                sumAddWalletUSD = float(df1['sumAddWalletUSD'][0])
            else:
                sumAddWalletUSD = 0.0
            if df1['sumAddWalletETH'][0] != None:
                sumAddWalletETH =  float(df1['sumAddWalletETH'][0])
            else:
                sumAddWalletETH = 0.0
            sql2 = f"SELECT COUNT(*) AS addCount FROM wallet_transaction W, transaction T WHERE W.trans_id = T.trans_id AND T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.wallet_trans_type = 'add'"
            df2 = pd.read_sql(sql2,conn)
            addCount = int(df2['addCount'][0])
            sql3 = f"SELECT COUNT(*) AS withdrawCount FROM wallet_transaction W, transaction T WHERE W.trans_id = T.trans_id AND T.trans_time > '{fromDate}' AND  T.trans_time < '{toDate}' AND W.wallet_trans_type = 'withdraw'"
            df3 = pd.read_sql(sql3,conn)
            withdrawCount = int(df3['withdrawCount'][0])
            res = {"totalAddedWalletAmountinUSD":sumAddWalletUSD,"totalAddedWalletAmountinETH":sumAddWalletETH,"totalWithdrawnWalletAmountinUSD":sumWithdrawWalletUSD,"totalWithdrawnWalletAmountinETH":sumWithdrawWalletETH,"totalAdds":addCount,"totalwithdraws":withdrawCount}
            return res
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
            if not df.empty:
                json_nft_data = df.to_json(orient = "index")
                parsed_json = json.loads(json_nft_data)
                for iter in parsed_json:
                    transTime = df['trans_time'][int(iter)]
                    transTimeDT = Timestamp.to_pydatetime(transTime)
                    parsed_json[iter].update({"trans_dateTime":str(transTimeDT)})
                return parsed_json
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)