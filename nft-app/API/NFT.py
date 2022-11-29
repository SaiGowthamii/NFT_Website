import config as cg
from flask import json
import pandas as pd

class NFT:

    def __init__(self,nft_name=None,token_id=None,contract_addr=None,owner_id=None,current_price=None) -> None:
        self.nft_name = nft_name
        self.token_id = token_id
        self.contract_addr = contract_addr
        self.owner_id = owner_id
        self.current_price = current_price
    
    def addNFT(self):
        conn = cg.connect_to_mySQL()
        try:
            cursor = conn.connect()
            if self.token_id == "" or self.token_id == None:
                res = {"res":"failed","message":"token id cannot be blank"}
                return json.dumps(res)
            if self.contract_addr == "" or self.contract_addr == None:
                res = {"res":"failed","message":"ethereum adddress cannot be blank"}
                return json.dumps(res)
            qry = f"SELECT t_id FROM trader where t_id = {self.owner_id}"
            df = pd.read_sql(qry,conn)
            if df.empty:
                res = {"res":"failed","message":"Cannot find user given id"}
                return json.dumps(res)
            qry = f"SELECT nft_name FROM nft WHERE token_id = '{self.token_id}' and contract_addr = '{self.contract_addr}'"
            df = pd.read_sql(qry,conn)
            if not df.empty:
                res = {"res":"failed","message":"nft with provided token_id and ethereum address already exists"}
                return json.dumps(res)
            qry1 = f"INSERT INTO nft(nft_name,token_id,contract_addr,owner_id,current_price) values('{self.nft_name}','{self.token_id}','{self.contract_addr}',{self.owner_id},{self.current_price})"
            cursor.execute(qry1)
            cursor.close()
            res = {"res":"success","message":"Created NFT Succcessfully"}
            return json.dumps(res)
        except Exception as e:
            res = {"res":"failed","message":str(e)}
            return json.dumps(res)