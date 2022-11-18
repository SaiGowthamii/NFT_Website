import config as cg
from flask import json
import pandas as pd

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
            qry1 = f"INSERT INTO test.user(username,password,user_type) VALUES ('{self.username}','{self.password}',{self.user_type})"
            cursor.execute(qry1)
            #cursor.commit()
            qry_id = f"SELECT uid FROM test.user WHERE username = '{self.username}' and password = '{self.password}'"
            df = pd.read_sql(qry_id,conn)
            t_id = int(df['uid'][0])
            qry2 = f"INSERT INTO test.trader(t_id,eth_addr,trader_level,fname,lname,email_id,cell_no,phone_no,street_addr,city,state,zip_code) VALUES ({t_id},'{self.eth_address}','{self.trader_level}','{self.first_name}','{self.last_name}','{self.email}','{self.cell_no}','{self.ph_no}','{self.street_addr}','{self.city}','{self.state}',{self.zip})"
            #user_type = cursor.fetchone()[0]
            cursor.execute(qry2)
            #cursor.commit()
            cursor.close()
            conn.close()
            #self.id = self.id + 1
            # user_type = cursor.fetchone()
        except Exception as e:
            print(e)    

    def createClient(self):
        conn = cg.connect_to_azure()
        try:
            cursor = conn.cursor()
            qry1 = f"INSERT INTO [dbo].[users](userid,username,pass_hash,type) VALUES ({self.id},'{self.username}','{self.password}','{self.type}')"
            qry2 = f"INSERT INTO [dbo].[trader](tid,fname,lname) VALUES ({id},'{self.first_name}',{self.last_name}')"
            #user_type = cursor.fetchone()[0]
            cursor.execute(qry1)
            cursor.execute(qry2)
            conn.commit()
            cursor.close()
            conn.close()
            self.id = self.id + 1
            # user_type = cursor.fetchone()
        except Exception as e:
            print(e) 

    def createManager(self):
        conn = cg.connect_to_azure()
        try:
            cursor = conn.cursor()
            qry1 = f"INSERT INTO [dbo].[users](userid,username,pass_hash,type) VALUES ({self.id},'{self.username}','{self.password}','{self.type}')"
            qry2 = f"INSERT INTO [dbo].[client](mid,fname,lname) VALUES ({id},'{self.first_name}','{self.last_name}')"
            #user_type = cursor.fetchone()[0]
            cursor.execute(qry1)
            cursor.execute(qry2)
            conn.commit()
            cursor.close()
            conn.close()
            self.id = self.id + 1
            # user_type = cursor.fetchone()
        except Exception as e:
            print(e)