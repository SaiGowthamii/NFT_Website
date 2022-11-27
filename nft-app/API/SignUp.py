import config as cg
from flask import json
import pandas as pd
from flask_bcrypt import generate_password_hash, check_password_hash

class SignUp:

    def __init__(self,first_name,last_name,eth_address,trader_level,email,cell_no,ph_no,street_addr,city,state,zip,username,password,user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.eth_address = eth_address
        self.trader_level = trader_level
        self.email = email
        self.ph_no = ph_no
        self.cell_no = cell_no
        self.type = type
        self.street_addr = street_addr
        self.city = city
        self.state = state
        self.zip = zip
        self.username = username
        self.password = password
        self.user_type = user_type
   

    def createTrader(self):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            qry = f"SELECT uid FROM user WHERE username = '{self.username}'"
            df = pd.read_sql(qry,conn)
            if not df.empty:
                res = {"res":"failed","message":"Username already exists"}
                return json.dumps(res)
            qry = f"SELECT eth_addr FROM trader WHERE eth_addr = '{self.eth_address}'"
            df = pd.read_sql(qry,conn)
            if not df.empty:
                res = {"res":"failed","message":"ethereum address already exists"}
                qry = f""
                return json.dumps(res)
            qry = f"SELECT email_id FROM trader WHERE email_id = '{self.email}'"
            df = pd.read_sql(qry,conn)
            if not df.empty:
                res = {"res":"failed","message":"email id already exists"}
                return json.dumps(res)
            self.password = generate_password_hash(self.password).decode('utf8')
            qry1 = f"INSERT INTO user(username,password,user_type) VALUES ('{self.username}','{self.password}',{self.user_type})"
            cursor.execute(qry1)
            qry_id = f"SELECT uid FROM user WHERE username = '{self.username}' and password = '{self.password}'"
            df = pd.read_sql(qry_id,conn)
            t_id = int(df['uid'][0])
            qry2 = f"INSERT INTO trader(t_id,eth_addr,trader_level,fname,lname,email_id,cell_no,phone_no,street_addr,city,state,zip_code) VALUES ({t_id},'{self.eth_address}','{self.trader_level}','{self.first_name}','{self.last_name}','{self.email}','{self.cell_no}','{self.ph_no}','{self.street_addr}','{self.city}','{self.state}',{self.zip})"
            cursor.execute(qry2)
            cursor.close()
            res = {"res":"success","message":"Created User Succcessfully"}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)