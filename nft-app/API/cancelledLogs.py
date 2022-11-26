import pandas as pd
from pandas.io import json
import config as cg
import sys
from datetime import datetime as dt


class cancelledLogs:
    def __init__(self,log_id=None,trans_id=None,log_info=None,log_trans_time=None):
        self.log_id = log_id
        self.trans_id = trans_id
        self.log_info = log_info
        self.log_trans_time = log_trans_time
    
    def addLogs(self):
        try:
            conn = cg.connect_to_mySQL()
            cursor = conn.connect()
            qry = f"INSERT INTO cancelledLogs (trans_id,log_info) VALUES ('{self.trans_id}','{self.log_info}')"
            cursor.execute(qry)
            print("inser into logs executed " ,file=sys.stderr)
            res = {"res":"success","message":"Created User Succcessfully"}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)

