import pandas as pd
from pandas.io import json
import config as cg
import time
from datetime import datetime as dt
import NFTTransaction
import sys
from pandas import Timestamp

class Transaction:

    def __init__(self,trans_type=None,trans_time=None):
        self.trans_type = trans_type
        self.trans_time = trans_time

    
    def cancelTransaction(self,transactionID,timestamp,logInfo):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            query1 = f"SELECT trans_time FROM transaction WHERE trans_id = {transactionID}"
            df1 = pd.read_sql(query1,conn)
            transTime = df1['trans_time'][0]
            transTimeDT = Timestamp.to_pydatetime(transTime)
            timeStampInt = int(float(timestamp)) 
            transTimeInt = int(dt.timestamp(transTimeDT) *1000)
            print(transTimeInt,file= sys.stderr)
            if (transTimeInt) > (timeStampInt):
                td = (transTimeInt) - (timeStampInt)
            else:
               td = (timeStampInt) - (transTimeInt)
            print(td,file= sys.stderr)
            if td <= 15*60*1000 :
                nftTransaction = NFTTransaction.NFTTransaction()
                out = nftTransaction.cancelNFTTransaction(transactionID,timestamp,logInfo)
                return json.dumps(out)
            else:
                res = {"res":"failed","message":"Unable to cancel Transaction : 15 min has elapsed"}
                return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

    def getTransAggregateInfo(self,fromDate,toDate):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            # get no of transactions
            sql1 = f"SELECT COUNT(*) as countTrans FROM transaction WHERE trans_time > '{fromDate}' AND  trans_time < '{toDate}'"
            df1 = pd.read_sql(sql1,conn)
            transCount = int(df1['countTrans'][0])
            sql2 = f"SELECT COUNT(*) as countNFT FROM transaction WHERE trans_time > '{fromDate}' AND  trans_time < '{toDate}' AND trans_type = 'nft'"
            df2 = pd.read_sql(sql2,conn)
            nftCount = int(df2['countNFT'][0])
            sql3 = f"SELECT COUNT(*) as countWallet FROM transaction WHERE trans_time > '{fromDate}' AND  trans_time < '{toDate}' AND trans_type = 'wallet'"
            df3 = pd.read_sql(sql3,conn)
            walletCount = int(df3['countWallet'][0])
            res = {"totalTransactions":transCount,"totalNFTTransactions":nftCount,"totalWalletTransaction":walletCount}
            return res

        except Exception as e:
            res = {"res":"failed","message":str(e)}



        
        

        
        


    