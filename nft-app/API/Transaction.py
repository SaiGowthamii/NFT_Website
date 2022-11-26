import pandas as pd
from pandas.io import json
import config as cg
import time
from datetime import datetime as dt
import NFTTransaction
import sys

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
            print((transTime.value),file=sys.stderr)
            timeStampInt = int(float(timestamp)) 
            transTimeInt = transTime.value
            print(type(transTimeInt),file=sys.stderr)
            if (transTimeInt) > (timeStampInt):
                td = (transTimeInt) - (timeStampInt)
            else:
               td = (timeStampInt) - (transTimeInt)
            print(td)
            if td > 15*60 :
                print("transaction update executed " ,file=sys.stderr)
                nftTransaction = NFTTransaction.NFTTransaction()
                out = nftTransaction.cancelNFTTransaction(transactionID,timestamp,logInfo)
                return json.dumps(out)
            else:
                res = {"res":"failed","message":"Unable to cancel Transaction : you will need to wait for 15 minutes"}
                return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)
        

        
        


    