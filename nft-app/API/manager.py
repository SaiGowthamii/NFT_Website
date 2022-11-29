import pandas as pd
from pandas.io import json
import config as cg
import sys
import cancelledLogs
from datetime import datetime as dt
from flask_bcrypt import generate_password_hash

class manager:
    def __init__(self,userName=None,password=None,fname = None,lname = None,manager_level=None):
        self.userName =  userName
        self.password = password
        self.fname = fname
        self.lname = lname
        self.manager_level = manager_level
       

    def createManager(self):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            qry = f"SELECT uid FROM user WHERE username = '{self.userName}'"
            df = pd.read_sql(qry,conn)
            if not df.empty:
                res = {"res":"failed","message":"Username already exists"}
                return res
            self.password = generate_password_hash(self.password).decode('utf8')
            qry1 = f"INSERT INTO user(username,password,user_type) VALUES ('{self.userName}','{self.password}',1)"
            cursor.execute(qry1)
            print("inserted into username",file=sys.stderr)
            qry_id = f"SELECT uid FROM user WHERE username = '{self.userName}' and password = '{self.password}'"
            df = pd.read_sql(qry_id,conn)
            manager_id = int(df['uid'][0])
            sql = f"INSERT INTO manager (t_id,fname,lname,manager_level) VALUES ({manager_id},'{self.fname}','{self.lname}',{self.manager_level})"
            cursor.execute(sql)
            cursor.close()
            res = {"res":"success","message":"Created Manager Succcessfully"}
            return res
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)



    
