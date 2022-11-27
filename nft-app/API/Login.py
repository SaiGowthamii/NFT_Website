import pandas as pd
from pandas.io import json
import config as cg
from flask import jsonify
import sys
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import Response, request
from flask_jwt_extended import create_access_token
import datetime

class Login:
    
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def check_type(self):
        conn = cg.connect_to_mySQL()
        #cursor = conn.cursor()
        query = f"SELECT * FROM user WHERE username='{self.username}'"
        #cursor.execute(chk)
        self.df1 = pd.read_sql(query,conn)
        #self.id = int(self.df1['userid'][0])
        # user_type = cursor.fetchone()[0]
        # cursor.execute(chk)
        # user_type = cursor.fetchone()
        #json_user_data = self.df1.to_json(orient = "index")
        #parsed_json = json.loads(json_user_data)
        #print(self.df1, file=sys.stderr)
        #print(self.df1.dtypes, file=sys.stderr)
        if not self.df1.empty:
            user_id = self.df1.at[0,'uid']
            psw_hash = self.df1['password'][0]
            ty = self.df1.at[0,'user_type']
            #print(type(psw), file=sys.stderr)
            #print(type(self.password), file=sys.stderr)
            #print(ty, file=sys.stderr)
            json_user_data = self.df1.to_json(orient = "index")
            parsed_json = json.loads(json_user_data)
            print(parsed_json, file=sys.stderr)
            if check_password_hash(psw_hash,self.password):
                return [user_id,ty,"success"]
            else:
                return [None,None,"failed"]
        else:
            return [None,None,"failed"]

    def get_trader_data(self,uid):
        conn = cg.connect_to_mySQL()
        qry = f"SELECT * FROM trader WHERE t_id={uid}"
        self.df2 = pd.read_sql(qry,conn)
        df3 = self.df1.join(self.df2)
        # user_type = cursor.fetchone()[0]
        # cursor.execute(chk)
        # user_type = cursor.fetchone()
        json_trader_data = df3.to_json(orient = "index")
        temp_json = json.loads(json_trader_data)
        parsed_json = temp_json["0"]
        parsed_json.update({"res":"success"})
        expires = datetime.timedelta(minutes=60)
        access_token = create_access_token(identity=str(uid), expires_delta=expires)
        parsed_json.update({"token":access_token})
        return json.dumps(parsed_json)
